import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { AppRoutingModule } from './app.routing.module';

// Components
import { AppComponent } from './app.component';
import { NavbarComponent } from './shared/navbar/navbar.component';
import { SidebarComponent } from './shared/sidebar/sidebar.component';
import { GalleryComponent } from './features/gallery/gallery-list/gallery.component';
import { DashboardComponent } from './features/dashboard/dashboard.component';
import { CommonModule } from '@angular/common';
import { SettingsComponent } from './features/settings/settings.component';
import { SearchComponent } from './shared/search/search.component';
import { LoginComponent } from './features/login/login.component';
import { AuthService } from './services/auth/auth.service';
import { AuthGuard } from './services/auth/auth.guard';
import { AuthInterceptor } from './services/auth/auth.intercepter';
import { UsersServices } from './services/user/user.service';
import { AlbumsServices } from './services/album/album.service';
import { GalleryViewComponent } from './features/gallery/gallery-view/gallery-view.component';

// Libraries
import {ToastModule} from 'ng2-toastr/ng2-toastr';
import { DashboardServices } from './services/dashboard/dashboard.service';



@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    SidebarComponent,
    GalleryComponent,
    DashboardComponent,
    SettingsComponent,
    SearchComponent,
    LoginComponent,
    GalleryViewComponent
  ],
  imports: [
    BrowserModule,
    CommonModule,
    FormsModule,
    HttpClientModule,
    AppRoutingModule,
    CommonModule,
    BrowserAnimationsModule,
    ToastModule.forRoot()
  ],
  providers: [
    AuthService,
    AuthGuard,
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true
    },
    UsersServices,
    AlbumsServices,
    DashboardServices
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
