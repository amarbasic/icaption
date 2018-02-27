import { Component, OnInit } from '@angular/core';
import { DashboardServices } from '../../services/dashboard/dashboard.service';

@Component({
    selector: 'app-dashboard',
    templateUrl: 'dashboard.component.html',
    styleUrls: ['dashboard.component.css']
})
export class DashboardComponent implements OnInit {

    dashboard_data: any = {
        "galleries": 0,
        "images": 0,
        "runs": 0,
        "notifications": []
    }

    constructor(private dashboardService: DashboardServices) { }

    ngOnInit(): void {
        this.dashboardService.getDashboard().subscribe(
            (res: any) => {
                console.log(res);
                this.dashboard_data = res;
            },
            (err: any) => {
                console.log(err);
            }
        )
    }

}
