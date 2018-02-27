import { Routes, RouterModule } from "@angular/router";
import { NgModule } from "@angular/core";

import { DashboardComponent } from "./features/dashboard/dashboard.component";
import { GalleryComponent } from "./features/gallery/gallery-list/gallery.component";
import { SettingsComponent } from "./features/settings/settings.component";
import { LoginComponent } from "./features/login/login.component";
import { AuthGuard } from "./services/auth/auth.guard";
import { GalleryViewComponent } from "./features/gallery/gallery-view/gallery-view.component";



const routes: Routes = [
    { path: '', component: DashboardComponent, canActivate: [AuthGuard] },
    { path: 'gallery', component: GalleryComponent, canActivate: [AuthGuard] },
    { path: 'gallery/:id', component: GalleryViewComponent, canActivate: [AuthGuard] },
    { path: 'settings', component: SettingsComponent, canActivate: [AuthGuard] },
    { path: 'login', component: LoginComponent },
    { path: '**', redirectTo: '', pathMatch: 'full' }
];

@NgModule({
    imports: [RouterModule.forRoot(routes, { useHash: true })],
    exports: [RouterModule],
    providers: []
})
export class AppRoutingModule { }