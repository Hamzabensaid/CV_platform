import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CvDetail } from './cv-detail';

describe('CvDetail', () => {
  let component: CvDetail;
  let fixture: ComponentFixture<CvDetail>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [CvDetail]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CvDetail);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
