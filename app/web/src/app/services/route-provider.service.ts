import { Injectable } from '@angular/core';

@Injectable()
export class RouteProviderService {

  public data: {
    key: string,
    value: any
  };

  constructor() { }

}
