import { Component } from '@angular/core';

@Component({
  selector: 'app-gallery',
  templateUrl: 'gallery.component.html',
  styles: []
})
export class GalleryComponent {
  albums: any = ["First", "Second", "Third", "Fourth", "Fifth"]
}
