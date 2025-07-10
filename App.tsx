import "./App.scss";

import type { ScreenViewport } from "@itwin/core-frontend";
import { FitViewTool, IModelApp, StandardViewId, IModelConnection } from "@itwin/core-frontend";
import { ColorDef } from "@itwin/core-common";
import { FillCentered } from "@itwin/core-react";
import { ECSchemaRpcInterface } from "@itwin/ecschema-rpcinterface-common";
import { ProgressLinear } from "@itwin/itwinui-react";
import { SmartPointerDecorator } from "./SmartPointerDecorator";
import {
  MeasurementActionToolbar,
  MeasureTools,
  MeasureToolsUiItemsProvider,
} from "@itwin/measure-tools-react";
import {
  AncestorsNavigationControls,
  CopyPropertyTextContextMenuItem,
  PropertyGridManager,
  PropertyGridUiItemsProvider,
  ShowHideNullValuesSettingsMenuItem,
} from "@itwin/property-grid-react";
import {
  CategoriesTreeComponent,
  createTreeWidget,
  ModelsTreeComponent,
  TreeWidget,
} from "@itwin/tree-widget-react";
import {
  useAccessToken,
  Viewer,
  ViewerContentToolsProvider,
  ViewerNavigationToolsProvider,
  ViewerPerformance,
  ViewerStatusbarItemsProvider,
} from "@itwin/web-viewer-react";
import React, { useCallback, useEffect, useMemo, useState } from "react";

import { Auth } from "./Auth";
import { history } from "./history";
import { getSchemaContext, unifiedSelectionStorage } from "./selectionStorage";
import { Point3d } from "@itwin/core-geometry";

// List your cow ECInstanceIds here
const cowIds = [
  "0x20000001c2",
  "0x20000001c3",
  "0x20000001c4",
];

// Static info for each cow
const staticCowInfo = [
  { id: "0x20000001c2", weightKg: 478, fattenedBy: "2025-08-12" },
  { id: "0x20000001c3", weightKg: 503, fattenedBy: "2025-09-01" },
  { id: "0x20000001c4", weightKg: 490, fattenedBy: "2025-08-25" },
];

// Query function
async function getCowPositionsById(iModel: IModelConnection, cowIds: string[]) {
  const cows: { id: string, position: Point3d }[] = [];
  for (const cowId of cowIds) {
    const query = `
      SELECT Origin
      FROM bis.GeometricElement3d
      WHERE ECInstanceId='${cowId}'
    `;
    for await (const row of iModel.query(query)) {
      if (row.origin) {
        cows.push({
          id: cowId,
          position: Point3d.create(row.origin.x, row.origin.y, row.origin.z),
        });
      }
    }
  }
  return cows;
}

const App: React.FC = () => {
  const [iModelId, setIModelId] = useState(process.env.IMJS_IMODEL_ID);
  const [iTwinId, setITwinId] = useState(process.env.IMJS_ITWIN_ID);
  const [changesetId, setChangesetId] = useState(
    process.env.IMJS_AUTH_CLIENT_CHANGESET_ID
  );

  const accessToken = useAccessToken();
  const authClient = Auth.getClient();

  const login = useCallback(async () => {
    try {
      await authClient.signInSilent();
    } catch {
      await authClient.signIn();
    }
  }, [authClient]);

  useEffect(() => {
    void login();
  }, [login]);

  useEffect(() => {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has("iTwinId")) {
      setITwinId(urlParams.get("iTwinId") as string);
    }
    if (urlParams.has("iModelId")) {
      setIModelId(urlParams.get("iModelId") as string);
    }
    if (urlParams.has("changesetId")) {
      setChangesetId(urlParams.get("changesetId") as string);
    }
  }, []);

  useEffect(() => {
    let url = `viewer?iTwinId=${iTwinId}`;
    if (iModelId) url = `${url}&iModelId=${iModelId}`;
    if (changesetId) url = `${url}&changesetId=${changesetId}`;
    history.push(url);
  }, [iTwinId, iModelId, changesetId]);

  // Set background color to sky blue in the view configuration
  const viewConfiguration = useCallback((viewPort: ScreenViewport) => {
    viewPort.view.displayStyle.backgroundColor = ColorDef.from(135, 206, 235); // Sky blue
    viewPort.invalidateScene();

    // Optionally fit view and set rotation
    void IModelApp.tools.run(FitViewTool.toolId, viewPort, true, false);
    viewPort.view.setStandardRotation(StandardViewId.Iso);
  }, []);

  const viewCreatorOptions = useMemo(
    () => ({ viewportConfigurer: viewConfiguration }),
    [viewConfiguration]
  );

  const onIModelAppInit = useCallback(async (iModel?: IModelConnection) => {
    await TreeWidget.initialize();
    await PropertyGridManager.initialize();
    await MeasureTools.startup();
    MeasurementActionToolbar.setDefaultActionProvider();

    if (!iModel) return;

    // Query positions
    const cowPositions = await getCowPositionsById(iModel, cowIds);

    // Merge static info
    const cowData = cowPositions.map(cow => {
      const extra = staticCowInfo.find(info => info.id === cow.id);
      return { ...cow, ...extra };
    });

    const decorator = new SmartPointerDecorator(cowData);
    IModelApp.viewManager.addDecorator(decorator);

    // Clean up decorator on unmount
    return () => {
      IModelApp.viewManager.dropDecorator(decorator);
    };
  }, []);

  return (
    <div className="viewer-container">
      {!accessToken && (
        <FillCentered>
          <div className="signin-content">
            <ProgressLinear indeterminate={true} labels={["Signing in..."]} />
          </div>
        </FillCentered>
      )}
      <Viewer
        iTwinId={iTwinId ?? ""}
        iModelId={iModelId ?? ""}
        changeSetId={changesetId}
        authClient={authClient}
        viewCreatorOptions={viewCreatorOptions}
        enablePerformanceMonitors={true}
        onIModelAppInit={onIModelAppInit}
        mapLayerOptions={{
          BingMaps: {
            key: "key",
            value: process.env.IMJS_BING_MAPS_KEY ?? "",
          },
        }}
        backendConfiguration={{
          defaultBackend: {
            rpcInterfaces: [ECSchemaRpcInterface],
          },
        }}
        uiProviders={[
          new ViewerNavigationToolsProvider(),
          new ViewerContentToolsProvider({
            vertical: {
              measureGroup: false,
            },
          }),
          new ViewerStatusbarItemsProvider(),
          {
            id: "TreeWidgetUIProvider",
            getWidgets: () => [
              createTreeWidget({
                trees: [
                  {
                    id: ModelsTreeComponent.id,
                    getLabel: () => ModelsTreeComponent.getLabel(),
                    render: (props) => (
                      <ModelsTreeComponent
                        getSchemaContext={getSchemaContext}
                        density={props.density}
                        selectionStorage={unifiedSelectionStorage}
                        selectionMode={"extended"}
                        onPerformanceMeasured={props.onPerformanceMeasured}
                        onFeatureUsed={props.onFeatureUsed}
                      />
                    ),
                  },
                  {
                    id: CategoriesTreeComponent.id,
                    getLabel: () => CategoriesTreeComponent.getLabel(),
                    render: (props) => (
                      <CategoriesTreeComponent
                        getSchemaContext={getSchemaContext}
                        density={props.density}
                        selectionStorage={unifiedSelectionStorage}
                        onPerformanceMeasured={props.onPerformanceMeasured}
                        onFeatureUsed={props.onFeatureUsed}
                      />
                    ),
                  },
                ],
              }),
            ],
          },
          new PropertyGridUiItemsProvider({
            propertyGridProps: {
              autoExpandChildCategories: true,
              ancestorsNavigationControls: (props) => (
                <AncestorsNavigationControls {...props} />
              ),
              contextMenuItems: [
                (props) => <CopyPropertyTextContextMenuItem {...props} />,
              ],
              settingsMenuItems: [
                (props) => (
                  <ShowHideNullValuesSettingsMenuItem
                    {...props}
                    persist={true}
                  />
                ),
              ],
            },
          }),
          new MeasureToolsUiItemsProvider(),
        ]}
        selectionStorage={unifiedSelectionStorage}
        getSchemaContext={getSchemaContext}
      />
    </div>
  );
};

export default App;