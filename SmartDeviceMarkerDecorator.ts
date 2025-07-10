import { Decorator, DecorateContext, Marker } from "@itwin/core-frontend";
import { Point3d } from "@itwin/core-geometry";

export interface CowData {
  id: string;
  position: Point3d;
  weightKg?: number;
  fattenedBy?: string;
}

export class SmartPointerDecorator implements Decorator {
  private _cowData: CowData[];

  constructor(cowData: CowData[]) {
    this._cowData = cowData;
  }

  public decorate(context: DecorateContext): void {
    for (const cow of this._cowData) {
      const marker = new Marker(
        new Point3d(cow.position.x, cow.position.y, cow.position.z + 2),
        { x: 60, y: 60 }
      );
      marker.title = `Cow ID: ${cow.id}`;
      marker.label = `Cow ID: ${cow.id}` +
        (cow.weightKg ? `\nWeight: ${cow.weightKg}kg` : "") +
        (cow.fattenedBy ? `\nFattened By: ${cow.fattenedBy}` : "");
      marker.labelFont = "bold 16px sans-serif";
      marker.labelOffset = { x: 0, y: -70 };
      marker.labelColor = "black";
      marker.addDecoration(context);
    }
  }
}