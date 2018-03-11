import { Injectable } from '@angular/core';
import { HttpHeaders, HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Observable } from 'rxjs/Observable';

@Injectable()
export class SearchService {
    private readonly _url: string;
    private headers = new HttpHeaders();

    constructor(private http: HttpClient) {
        this._url = environment.serverUrl + '/albums/';
        this.headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    }

  getSearchImagesId(text): Observable<any> {
    var url = this._url + 'search';
    return this.http.post(url, {"caption": text});
}

}
