import { Component, OnInit, OnDestroy } from '@angular/core';
import { DashboardServices } from '../../services/dashboard/dashboard.service';

@Component({
    selector: 'app-dashboard',
    templateUrl: 'dashboard.component.html',
    styleUrls: ['dashboard.component.css']
})
export class DashboardComponent implements OnInit, OnDestroy {

    dashboard_data: any = {
        "galleries": 0,
        "images": 0,
        "runs": 0,
        "notifications": []
    }

    interval: any;

    constructor(private dashboardService: DashboardServices) { }

    ngOnInit(): void {
        this.refreshDashboard();
        this.interval = setInterval(() => { 
            this.refreshDashboard(); 
        }, 5000);
    }

    ngOnDestroy() {
        clearInterval(this.interval);
    }

    refreshDashboard() {
        this.dashboardService.getDashboard().subscribe(
            (res: any) => {
                console.log("Data from dashboard");
                this.dashboard_data = res;
            },
            (err: any) => {
                console.log(err);
            }
        )
    }

}
