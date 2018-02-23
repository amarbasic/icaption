import { Component, OnInit } from '@angular/core';
import { AlbumsServices } from '../../services/album/album.service';
import { NewAlbumModel, AlbumModel } from '../../models/album.model';

@Component({
  selector: 'app-gallery',
  templateUrl: 'gallery.component.html',
  styles: []
})
export class GalleryComponent implements OnInit {
  newAlbumModel: NewAlbumModel;
  albums: any[];

  constructor(private albumService: AlbumsServices) {
    this.newAlbumModel = new NewAlbumModel();
  }

  ngOnInit() {
    this.albumService.getAlbums().subscribe(
      (res: any) => {
        console.log(res);
        this.albums = res
      },
      (err: any) => {
        console.log(err);
      }
    );
  }

  create() {
    console.log(this.newAlbumModel);
    this.albumService.insertAlbum(this.newAlbumModel).subscribe(
      (res:any) => {
        console.log(res);
      },
      (err: any) => {
        console.log(err);
      }
    );
  }
}
