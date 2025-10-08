import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CvList } from './cv-list';

describe('CvList', () => {
  let component: CvList;
  let fixture: ComponentFixture<CvList>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CvList]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CvList);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
