import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CvForm } from './cv-form';

describe('CvForm', () => {
  let component: CvForm;
  let fixture: ComponentFixture<CvForm>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [CvForm]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CvForm);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
