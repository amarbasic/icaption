import { Component, ViewContainerRef } from '@angular/core';
import { LoginModel } from '../../models/login.model';
import { UsersServices } from '../../services/user/user.service';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth/auth.service';
import { RegistrationModel } from '../../models/registration.model';
import { ToastsManager } from 'ng2-toastr';


@Component({
    selector: 'app-login',
    templateUrl: 'login.component.html',
    styleUrls: ['login.component.css']
})
export class LoginComponent {

    loginModel: LoginModel;
    registrationModel: RegistrationModel

    constructor(private userService: UsersServices,
        private router: Router,
        private authService: AuthService,
        public toastr: ToastsManager, vcr: ViewContainerRef) {
        this.loginModel = new LoginModel();
        this.registrationModel = new RegistrationModel();
        this.toastr.setRootViewContainerRef(vcr);
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
                localStorage.setItem('username', res.body.username);
                this.router.navigateByUrl('/');
            },
            (err: any) => {
                console.log(err);
                if (err.error)
                    this.toastr.error(err.error, 'Something went wrong!');
                else this.toastr.error("Please try again", 'Something went wrong!');
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
                this.toastr.success('Your registration was successful. Please login', 'Success!');
            },
            (err: any) => {
                if (err.error)
                    this.toastr.error(err.error, 'Something went wrong!');
                else this.toastr.error("Please try again", 'Something went wrong!');
            }
        )
    }
}