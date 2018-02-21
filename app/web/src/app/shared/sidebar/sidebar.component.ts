import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

declare var $: any;

export interface RouteInfo {
    path: string;
    title: string;
    icon: string;
    class: string;
}

export const ROUTES: RouteInfo[] = [
    { path: 'dashboard', title: 'Dashboard', icon: 'fa fa-tachometer', class: '' },
    { path: 'gallery', title: 'Gallery', icon: 'fa fa-picture-o', class: '' },
];

@Component({
    selector: 'app-sidebar',
    templateUrl: 'sidebar.component.html'
})


export class SidebarComponent {
    public menuItems: any[];

    constructor(private router: Router) { }

    ngOnInit() {
        this.menuItems = ROUTES.filter(menuItem => menuItem);
    }
}