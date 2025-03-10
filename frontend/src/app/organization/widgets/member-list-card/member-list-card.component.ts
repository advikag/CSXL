import { Component, Input } from '@angular/core';
import { MemberService } from '../../member-page/member.service';

@Component({
  selector: 'app-member-list-card',
  templateUrl: './member-list-card.component.html',
  styleUrls: ['./member-list-card.component.css']
})
export class MemberListCardComponent {
  @Input() memberDetails: any;
  @Input() leaderDetails: any;
}
