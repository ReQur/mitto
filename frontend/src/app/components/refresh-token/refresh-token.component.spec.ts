import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RefreshTokenComponent } from './refresh-token.component';

describe('RefreshTokenComponent', () => {
  let component: RefreshTokenComponent;
  let fixture: ComponentFixture<RefreshTokenComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [RefreshTokenComponent]
    });
    fixture = TestBed.createComponent(RefreshTokenComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
