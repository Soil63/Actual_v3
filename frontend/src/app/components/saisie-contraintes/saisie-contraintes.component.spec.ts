import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SaisieContraintesComponent } from './saisie-contraintes.component';

describe('SaisieContraintesComponent', () => {
  let component: SaisieContraintesComponent;
  let fixture: ComponentFixture<SaisieContraintesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SaisieContraintesComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SaisieContraintesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
