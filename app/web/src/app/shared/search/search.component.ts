import { Component } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { RouteProviderService } from '../../services/route-provider.service';

@Component({
    selector: 'app-search',
    templateUrl: 'search.component.html'
})

export class SearchComponent {

    model = {
        "description": null
    }

    constructor(private router: Router, private storage: RouteProviderService) {
    }

    onSubmit() {
        console.log(this.model);
        this.storage.data = {
            key: "search",
            value: this.model.description
        };
        this.router.navigateByUrl("search");
    }
 }