import { Component, OnInit, ViewContainerRef } from '@angular/core';
import { AlbumsServices } from '../../../services/album/album.service';
import { NewAlbumModel, AlbumModel } from '../../../models/album.model';
import { Router, ActivatedRoute } from '@angular/router';
import { ToastsManager } from 'ng2-toastr';

@Component({
  selector: 'app-gallery',
  templateUrl: 'gallery.component.html',
  styleUrls: ['gallery.component.css']
})
export class GalleryComponent implements OnInit {
  newAlbumModel: NewAlbumModel;
  albums: AlbumModel[];
  private sub: any;

  constructor(private albumService: AlbumsServices, private router: Router,
    public toastr: ToastsManager, vcr: ViewContainerRef, private route: ActivatedRoute) {
    this.newAlbumModel = new NewAlbumModel();
    this.toastr.setRootViewContainerRef(vcr);
  }

  ngOnInit() {

    this.sub = this.route.queryParams.subscribe(params => {
      var message = params['message'];
      if (message) this.toastr.success(message, "Success!");
    });


    this.albumService.getAlbums().subscribe(
      (res: any) => {
        this.albums = res
        console.log(res);
      },
      (err: any) => {
        console.log(err);
        if (err.error)
          this.toastr.error(err.error, 'Something went wrong!');
        else this.toastr.error("Please try again", 'Something went wrong!');
      }
    );
  }

  ngOnDestroy() {
    this.sub.unsubscribe();
  }

  create() {
    this.albumService.insertAlbum(this.newAlbumModel).subscribe(
      (res: any) => {
        this.albums.push(res);
        this.toastr.success('New gallery created.', 'Success!');
      },
      (err: any) => {
        if (err.error)
          this.toastr.error(err.error, 'Something went wrong!');
        else this.toastr.error("Please try again", 'Something went wrong!');
      }
    );
  }

  showGallery(album_id) {
    this.router.navigateByUrl("gallery/" + album_id);
  }
}
