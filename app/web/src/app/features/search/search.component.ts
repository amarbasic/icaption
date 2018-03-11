import { Component, OnInit, ViewContainerRef } from '@angular/core';
import { SearchService } from '../../services/search.service';
import { Router } from '@angular/router';
import { ToastsManager } from 'ng2-toastr';

@Component({
  selector: 'app-searched',
  templateUrl: "search.component.html",
  styleUrls: ["search.component.css"]
})
export class SearchComponent implements OnInit {

  model = {
    "description": null
  }
  images: any;

  constructor(private searchService: SearchService, private router: Router, public toastr: ToastsManager, vcr: ViewContainerRef) {
    this.toastr.setRootViewContainerRef(vcr);
  }

  ngOnInit() { }

  onSubmit() {
    this.searchService.getSearchImagesId(this.model.description).subscribe(
      (res: any) => {
        console.log(res);
        this.images = res.images;
      },
      (err: any) => {
        if (err.error)
          this.toastr.error(err.error, 'Something went wrong!');
        else this.toastr.error("Please try again", 'Something went wrong!');
      }
    )

  }

  navigateToGallery(album_id) {
    this.router.navigateByUrl("gallery/" + album_id);
  }
}
