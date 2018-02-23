import { Component } from '@angular/core';
import { LoginModel } from '../../models/login.model';
import { UsersServices } from '../../services/user/user.service';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth/auth.service';
import { RegistrationModel } from '../../models/registration.model';


@Component({
    selector: 'app-login',
    templateUrl: 'login.component.html',
    styleUrls: ['login.component.css']
})
export class LoginComponent {

    loginModel: LoginModel;
    registrationModel: RegistrationModel

    constructor(private userService: UsersServices, private router: Router, private authService: AuthService) {
        this.loginModel = new LoginModel();
        this.registrationModel = new RegistrationModel();
    }

    ngOnInit() {
        if (this.isLoggedIn()) this.router.navigateByUrl('/');
      }

    private isLoggedIn() {
        return localStorage.getItem("auth_token") != undefined;
      }

    login() {
        console.log(this.loginModel);
        this.loginModel.password = btoa(this.loginModel.password);
        this.authService.login(this.loginModel).subscribe(
            (res: any) => {
                localStorage.setItem('auth_token', res.body.token);
                this.router.navigateByUrl('/');
            },
            (err: any) => {
                console.log(err);
                this.loginModel.password = "";
            }
        )

    }

    registration() {
        console.log(this.registrationModel);
        this.registrationModel.password = btoa(this.registrationModel.password);
        this.registrationModel.password_confirmation = btoa(this.registrationModel.password_confirmation);
        this.userService.insertUser(this.registrationModel).subscribe(
            (res: any) => {
                console.log(res);
            },
            (err: any) => {
                console.log(err);
            }
        )
    }
}