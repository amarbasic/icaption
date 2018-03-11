import { Component, OnInit } from '@angular/core';
import { RouteProviderService } from '../../services/route-provider.service';

@Component({
  selector: 'app-searched',
  templateUrl: "searched.component.html",
  styles: []
})
export class SearchedComponent implements OnInit {

  constructor(private storage: RouteProviderService) { }

  ngOnInit() {
    console.log(this.storage.data);
  }

}
