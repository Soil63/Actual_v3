import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ModifBenevComponent } from './modif-benev.component';

describe('ModifBenevComponent', () => {
  let component: ModifBenevComponent;
  let fixture: ComponentFixture<ModifBenevComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ModifBenevComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ModifBenevComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
