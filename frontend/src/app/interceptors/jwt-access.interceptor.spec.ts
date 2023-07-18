import { TestBed } from '@angular/core/testing';

import { JwtAccessInterceptor } from './jwt-access.interceptor';

describe('JwtAccessInterceptor', () => {
  beforeEach(() => TestBed.configureTestingModule({
    providers: [
      JwtAccessInterceptor
      ]
  }));

  it('should be created', () => {
    const interceptor: JwtAccessInterceptor = TestBed.inject(JwtAccessInterceptor);
    expect(interceptor).toBeTruthy();
  });
});
