import { Component, OnInit } from '@angular/core';
import { AlbumsServices } from '../../../services/album/album.service';
import { NewAlbumModel, AlbumModel } from '../../../models/album.model';
import { Router } from '@angular/router';

@Component({
  selector: 'app-gallery',
  templateUrl: 'gallery.component.html',
  styleUrls: ['gallery.component.css']
})
export class GalleryComponent implements OnInit {
  newAlbumModel: NewAlbumModel;
  albums: AlbumModel[];

  constructor(private albumService: AlbumsServices, private router: Router) {
    this.newAlbumModel = new NewAlbumModel();
  }

  ngOnInit() {
    this.albumService.getAlbums().subscribe(
      (res: any) => {
        this.albums = res
        console.log(res);
      },
      (err: any) => {
        console.log(err);
      }
    );
  }

  create() {
    this.albumService.insertAlbum(this.newAlbumModel).subscribe(
      (res:any) => {
        this.albums.push(res);
      },
      (err: any) => {
        console.log(err);
      }
    );
  }

  showGallery(album_id) {
    this.router.navigateByUrl("gallery/" + album_id);
  }
}
