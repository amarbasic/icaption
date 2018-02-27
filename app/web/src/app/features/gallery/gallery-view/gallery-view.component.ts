import { Component, OnInit, OnDestroy, ChangeDetectorRef } from "@angular/core";
import { ActivatedRoute, Router } from "@angular/router";
import { AlbumsServices } from "../../../services/album/album.service";


@Component({
    selector: 'app-gallery-view',
    templateUrl: 'gallery-view.component.html',
    styleUrls: ['gallery-view.component.css']
})
export class GalleryViewComponent implements OnInit, OnDestroy {

    id: number;
    private sub: any;
    album: any = {
        "name": "",
        "images": []
    };
    image: any;

    path = '';  
    public file_srcs: string[] = [];  
    public debug_size_before: string[] = [];  
    public debug_size_after: string[] = [];  

    constructor(private router: Router, private route: ActivatedRoute, private albumService: AlbumsServices, private changeDetectorRef: ChangeDetectorRef) { }

    ngOnInit() {
        this.sub = this.route.params.subscribe(params => {
            this.id = +params['id'];
            console.log("Get images for " + this.id);
            this.albumService.getAlbumImages(this.id).subscribe(
                (res: any) => {
                    this.album = res;
                },
                (err: any) => {
                    console.log(err);
                }
            );
        });
    }

    ngOnDestroy() {
        this.sub.unsubscribe();
    }

    create() {
        this.albumService.insertAlbumImages(this.id, {"images": this.file_srcs}).subscribe(
            (res: any) => {
                res.forEach(element => {
                    this.album.images.push(element);
                });
                this.file_srcs = []
            },
            (err: any) => {
                console.log(err);
            }
        );

    }

    deleteGallery(album_id) {
        this.albumService.deleteAlbum(album_id).subscribe(
            (res: any) => {
                console.log(res);
                this.router.navigateByUrl("/gallery");
            },
            (err: any) => {
                console.log(err);
            }
        );
    }

    deleteImage(image_id) {
        this.albumService.deleteImage(image_id).subscribe(
            (res: any) => {
                console.log(res);
                this.album.images = this.album.images.filter(image => image.id != image_id);
            },
            (err: any) => {
                console.log(err);
            }
        );
    }

    fileChange(input) {  
        this.readFiles(input.files);  
    }  
    readFile(file, reader, callback) {  
        reader.onload = () => {  
            callback(reader.result);  
            this.image = reader.result;  
        }  
        reader.readAsDataURL(file);  
    }  
    readFiles(files, index = 0) {  
        // Create the file reader  
        let reader = new FileReader();  
        // If there is a file  
        if (index in files) {  
            // Start reading this file  
            this.readFile(files[index], reader, (result) => {  
                // Create an img element and add the image file data to it  
                var img = document.createElement("img");  
                img.src = result;  
                // Send this img to the resize function (and wait for callback)  
                this.resize(img, 250, 250, (resized_jpeg, before, after) => {  
                    // For debugging (size in bytes before and after)  
                    this.debug_size_before.push(before);  
                    this.debug_size_after.push(after);  
                    // Add the resized jpeg img source to a list for preview  
                    // This is also the file you want to upload. (either as a  
                    // base64 string or img.src = resized_jpeg if you prefer a file).  
                    this.file_srcs.push(resized_jpeg);  
                    // Read the next file;  
                    this.readFiles(files, index + 1);  
                });  
            });  
        } else {  
            // When all files are done This forces a change detection  
            this.changeDetectorRef.detectChanges();  
        }  
    }  
    resize(img, MAX_WIDTH: number, MAX_HEIGHT: number, callback) {  
        // This will wait until the img is loaded before calling this function  
        return img.onload = () => {  
            // Get the images current width and height  
            var width = img.width;  
            var height = img.height;  
            // Set the WxH to fit the Max values (but maintain proportions)  
            if (width > height) {  
                if (width > MAX_WIDTH) {  
                    height *= MAX_WIDTH / width;  
                    width = MAX_WIDTH;  
                }  
            } else {  
                if (height > MAX_HEIGHT) {  
                    width *= MAX_HEIGHT / height;  
                    height = MAX_HEIGHT;  
                }  
            }  
            // create a canvas object  
            var canvas = document.createElement("canvas");  
            // Set the canvas to the new calculated dimensions  
            canvas.width = width;  
            canvas.height = height;  
            var ctx = canvas.getContext("2d");  
            ctx.drawImage(img, 0, 0, width, height);  
            // Get this encoded as a jpeg  
            // IMPORTANT: 'jpeg' NOT 'jpg'  
            var dataUrl = canvas.toDataURL('image/jpeg');  
            // callback with the results  
            callback(dataUrl, img.src.length, dataUrl.length);  
        };  
    }  
}