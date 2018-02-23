import { Injectable } from "@angular/core";
import { HttpHeaders, HttpClient } from "@angular/common/http";
import { environment } from "../../../environments/environment";
import { Observable } from "rxjs/Observable";
import { NewAlbumModel, AlbumModel } from "../../models/album.model";


@Injectable()
export class AlbumsServices {

    private readonly _url: string;
    private headers = new HttpHeaders();

    constructor(private http: HttpClient) {
        this._url = environment.serverUrl + '/albums';
        this.headers = new HttpHeaders({ 'Content-Type': 'application/json' });
    }

    insertAlbum(album:NewAlbumModel): Observable<any> {
        var url = this._url + '/new';
        return this.http.post(url, album);
    }

    getAlbums(): Observable<any> {
        return this.http.get(this._url);
    }

}