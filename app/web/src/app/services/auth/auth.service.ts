import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { HttpHeaders } from "@angular/common/http";
import { environment } from "../../../environments/environment";
import { Observable } from "rxjs/Observable";
import { LoginModel } from "../../models/login.model";


@Injectable()
export class AuthService {

    private readonly _url: string;
    private headers = new HttpHeaders();
    
    constructor(private http: HttpClient) { 
        this._url = environment.serverUrl + '/users';
        this.headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    }

    login(loginModel:LoginModel): Observable<any> {
        return this.http.post(this._url + '/login', loginModel, {
            headers: this.headers,
            observe: 'response'
        });
    }

    logout() {
        localStorage.removeItem("auth_token");
    }

    authenticated() {
        return localStorage.getItem("auth_token") != null;
      }
}
