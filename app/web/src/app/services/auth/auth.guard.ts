import { CanActivate } from "@angular/router";
import { Router } from '@angular/router';
import { AuthService } from "./auth.service";
import { Injectable } from "@angular/core";

@Injectable()
export class AuthGuard implements CanActivate {
    constructor(private authService: AuthService, private router: Router) { }
    canActivate() {
        console.log("Call Guard -> " + localStorage.getItem("auth_token"));
        if(localStorage.getItem("auth_token") != null) return true;
        this.router.navigateByUrl('/login');
    }
}
