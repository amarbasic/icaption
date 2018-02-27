import { Injectable } from "@angular/core";
import { HttpHeaders, HttpClient } from "@angular/common/http";
import { environment } from "../../../environments/environment";
import { Observable } from "rxjs/Observable";

@Injectable()
export class DashboardServices {

    private readonly _url: string;
    private headers = new HttpHeaders();

    constructor(private http: HttpClient) {
        this._url = environment.serverUrl + '/dashboard/';
        this.headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    }

    getDashboard(): Observable<any> {
        return this.http.get(this._url);
    }
}