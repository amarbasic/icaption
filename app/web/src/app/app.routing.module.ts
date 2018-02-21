import { Routes, RouterModule } from "@angular/router";
import { NgModule } from "@angular/core";

import { DashboardComponent } from "./features/dashboard/dashboard.component";
import { GalleryComponent } from "./features/gallery/gallery.component";
import { SettingsComponent } from "./features/settings/settings.component";



const routes: Routes = [
    { path: '', component: DashboardComponent },
    { path: 'gallery', component: GalleryComponent },
    { path: 'settings', component: SettingsComponent },
    { path: '**', redirectTo: '', pathMatch: 'full' }
];

@NgModule({
    imports: [RouterModule.forRoot(routes, { useHash: true })],
    exports: [RouterModule],
    providers: []
})
export class AppRoutingModule { }