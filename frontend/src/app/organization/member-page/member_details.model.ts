import { Organization } from '../organization.model';
import { Profile } from 'src/app/profile/profile.service';

export interface MemberDetails {
  memberId: Number;
  organization_id: Number;
  user_id: Number;
  approval_status: Boolean;
  admin_status: Boolean;
  member_type: MembershipType;
  term: String;
  user: Profile;
  title: String;
}

enum MembershipType {
  MEMBER = 0,
  LEADER = 1
}
