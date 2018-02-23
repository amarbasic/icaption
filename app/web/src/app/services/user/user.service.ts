import { Injectable } from "@angular/core";
import { HttpHeaders, HttpClient } from "@angular/common/http";
import { environment } from "../../../environments/environment";
import { Observable } from "rxjs/Observable";
import { RegistrationModel } from "../../models/registration.model";


@Injectable()
export class UsersServices {

    private readonly _url: string;
    private headers = new HttpHeaders();

    constructor(private http: HttpClient) {
        this._url = environment.serverUrl + '/users';
        this.headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    }

    insertUser(user:RegistrationModel): Observable<any> {
        var url = this._url + '/new';
        return this.http.post(url, user);
    }

}