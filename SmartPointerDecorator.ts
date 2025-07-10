import {
  DecorateContext,
  Decorator,
  GraphicType,
  IModelApp
} from "@itwin/core-frontend";
import { Point3d } from "@itwin/core-geometry";
import { ColorDef } from "@itwin/core-common";

export class SmartPointerDecorator implements Decorator {
  public decorate(context: DecorateContext): void {
    const builder = context.createGraphicBuilder(GraphicType.WorldOverlay);

    // Place a marker at X, Y, Z location — replace with real coordinates
    const point = Point3d.create(50, 75, 0); // example location
    builder.setSymbology(ColorDef.fromString("red"), ColorDef.white, 1);
    builder.addSphere(point, 2); // adds a small red sphere

    context.addDecorationFromBuilder(builder);
  }
}
