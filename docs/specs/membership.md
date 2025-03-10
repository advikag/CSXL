# Member Roster Technical Specifications:

This document contains the technical specifications, including sample data representation of our feature, descriptions of underlying database / entity-level representation decisions and development concerns. By reading this, you should be able to replicate how we add and delete organization members, view and edit members/leader details, provide administrative status and leader status to members, and change the term of an organization. 

## Authors:
- [Advika Ganesh](https://github.com/advikag)
- [Erin Ma](https://github.com/erinma6)
- [Lalitha Vadrevu](https://github.com/vlalithaunc)
- [Pallavi Sastry](https://github.com/pallavi-sastry)


# How do I know if the organization is accepting members?

A new feature has been added to both the organization's card as well as the organization details page. Each organization card has an open and closed indicator which displays the word open if the organization is accepting members and closed if the organization is not accepting members.

![](https://lh7-us.googleusercontent.com/RYtX1GWafP4ohD4rqK4n_LWAsiLWK5sHOE6G5seaLK7xjXkGcaMVADWIZE9eP4Sp5ACykxUao7YShSvQuOBSNMl5taUtT3d5-OMIDkx1FxBubyC4JzBGYqMZV6m5Gd4MGD11guRo_F0yZon_y_Kpvrg)

# How to open or close membership for an organization?

In the organization editor component there is a toggle that allows the admin of an organization to decide whether the organization is accepting members or not.On clicking the details button of each organization there is another indicator that denotes whether the club is open or closed.

![](https://lh7-us.googleusercontent.com/lj4S3sXU_05JuLMGmUvhAj9q8lev8tFu4CWrhuMnrzJvx6hIIoGxjZVIpSF-PW1xlyyAl4DkJvr74PLs3iBoKVvLknkgFBofIGn-kHl_Sds2nM7HC2ZMFV9rxAZ_y4jap2BSXZJRrVhSthInIM1wc_c)

If the toggle is turned off, the indicator changes to closed and the request button is disabled, not allowing any members into the organization.

![](https://lh7-us.googleusercontent.com/sqnsy74qCZDgLGGbpz5OxPzeJ1LocIpocXRvXp8928E6IjgBgAaKLvL7LwHfhrrbqZ78UCDztqHYy35qcKhvuR3Po5rdYH3Mwl8Bjlg3-QNLLIhwo4MX2h3zVKFxBhHq3OYQTB3v-1uqnDLWGVCMKEc)


In addition, if the toggle for external application required is set on, on requesting membership into the organization,a snack bar appears with the message that states an external application is required.


# How do I become a member of an organization?

-   From the sidebar, click on Organizations

-   Click the details button of the desired organization

-   Click the request membership button in order to request membership into an organization.![](https://lh7-us.googleusercontent.com/wiAkXtvZ1LGUYajRj0UhUlbxN2K-j9_i4FCkKVcWz8EkBhSSMJp13vky4h6tzuVhUAPfZCmFXlH7RXac7tmeTL73iGVFJOhzh9-iGNMxgAQimYlmc6q7JKddmxd7sTXcdNco8hIq8gqqbjape4cPGZs)

# How do I edit the details of a member:


Anyone with admin privileges has the ability to edit the details of a member.They have the power to add a leadership title, grant and remove admin privileges, and make or revoke a member as a leader.

![](https://lh7-us.googleusercontent.com/_xH5EE9qazaiHQo4F1Ef1IHk6m1glLCuzF1qUEsCfWoMpK2iSv5QCp7171Kb-jrD2eDSF5hxv2TmPasR__VhtoXeuPug-RJvJVzEweO5JVd-oLU4gFboxujhr3KeoecI8dqoSEzVSdJxlqcrppWXJvo)

# How do I view the members and leaders of an organization?

-   In the organization page, click on the details button of the desired organization.

-   On clicking the members button, We have created a member view page that displays the members and leaders of the club.![](https://lh7-us.googleusercontent.com/fm7jAAyXF6eIEzki-OAlYx2fhaf9OObe32X173p6xNCWcoCSGfj5kDuWAhVjgjd7ddM_PHPqNTPi5F1qlPAZeGvft9zW4JcZ-6CCtot_ioCODKu9Zhq-aUuynDI2nFYZozBErgdTUeb0ipTaOa1wId8)


# How do I add or remove members or admins of an organization?


The admin of an organization has the ability to edit details about the members of an organization.The admin will see an edit icon for each member of the club that allows them to grant or remove admin and leadership positions in the organization.

![](https://lh7-us.googleusercontent.com/RLkPe_d2bFN2glzP4z8RcfDoYWgs2ZW6OWvbp98D1wTypjstfGuMRFUyTpkreSjqT5V2YtMGFBDKFWATSHoPTdKzN3o0jEah8WknDCpea0kcTBVsiWsHNy-xNGMP8H7yoW75dNM5iZe3CdoKhi_m4ak)

# How do I view members by term?


At the bottom of the organization editor, find the dropdown for 'Select Term'. Through clicking this button you can members across various terms.

![](https://lh7-us.googleusercontent.com/niY-8l3pJJLTFz1OON973mWSdhoO5Vy8YjCvNwtZVqoXxOOtHoFOtqQwis0EujHmcokC96H3Gz7W5zUoNpAL1nTs1u5Gys6zdqGFkKJvcxVDVvT9ARLxzaMC29p2w0FMjLWzSX81AgmtZP4phCiPKSE)

After selection of FA24, viewers will be able to see the member roster for Fall 2024![](https://lh7-us.googleusercontent.com/YpK0ftfX12CRCoWpb0A6KYxECSjsg7DCe7VoJdq6z9BqxPdPPA_Y7lTP66rQiptdP_Bp6IMdcd4LwNzXh2tdQeTaDSsyMGP9UGC72THyjDgjITxjYhDN6O2tdd0BQEulNY2iVAR2ZvDDkpOgFQ-91Uk)

# Backend Service Functions:

We employed the use of various functions in order to retrieve and update values from the member database:

-   get_member_details: this function returns the MemberDetails model of all the members in an organization

<https://github.com/comp423-24s/csxl-final-team-a3/blob/8c6bd2803d73f1edc2c71326b0a8e97ad7ed0609/backend/services/member.py#L102-L129>

-   new_member: this function adds a member request to the member database

<https://github.com/comp423-24s/csxl-final-team-a3/blob/8c6bd2803d73f1edc2c71326b0a8e97ad7ed0609/backend/services/member.py#L180-L222>

-   approve_member: this function changes the approvalStatus field from False to True, in order to approve a user's membership into an organization.

<https://github.com/comp423-24s/csxl-final-team-a3/blob/8c6bd2803d73f1edc2c71326b0a8e97ad7ed0609/backend/services/member.py#L69-L100>

-   get_approved_member_details: this function fetches the MemberDetails of the approved members of the organization <https://github.com/comp423-24s/csxl-final-team-a3/blob/8c6bd2803d73f1edc2c71326b0a8e97ad7ed0609/backend/services/member.py#L131-L151>

-   get_pending_member_details: this function fetches the MemberDetails of the members that have requested membership but haven't been approved yet, for example approvalStatus of 'False'

<https://github.com/comp423-24s/csxl-final-team-a3/blob/8c6bd2803d73f1edc2c71326b0a8e97ad7ed0609/backend/services/member.py#L153-L178>

-   delete_member: this function deletes the selected member from the organization

<https://github.com/comp423-24s/csxl-final-team-a3/blob/8c6bd2803d73f1edc2c71326b0a8e97ad7ed0609/backend/services/member.py#L180-L222>

-   make_admin: this function makes the selected member an admin of the organization

<https://github.com/comp423-24s/csxl-final-team-a3/blob/8c6bd2803d73f1edc2c71326b0a8e97ad7ed0609/backend/services/member.py#L261-L303>

-   remove_admin: this function removes the admin privileges of the member 

<https://github.com/comp423-24s/csxl-final-team-a3/blob/8c6bd2803d73f1edc2c71326b0a8e97ad7ed0609/backend/services/member.py#L261-L303>

-   get_member_by_id: this function fetches the member of an organization based on their member

<https://github.com/comp423-24s/csxl-final-team-a3/blob/8c6bd2803d73f1edc2c71326b0a8e97ad7ed0609/backend/services/member.py#L344-L374>

-   make_leader: this function makes the selected user a leader of the organization

<https://github.com/comp423-24s/csxl-final-team-a3/blob/8c6bd2803d73f1edc2c71326b0a8e97ad7ed0609/backend/services/member.py#L376-L408>

-   get_leader_details: this function retrieves the details of the leader of an organization

<https://github.com/comp423-24s/csxl-final-team-a3/blob/8c6bd2803d73f1edc2c71326b0a8e97ad7ed0609/backend/services/member.py#L410-L429>

-   get_member_details_by_term: this function retrieves the details of the member of an organization based on the term

<https://github.com/comp423-24s/csxl-final-team-a3/blob/8c6bd2803d73f1edc2c71326b0a8e97ad7ed0609/backend/services/member.py#L431-L460>

-   remove_leader:  this function removes the selected member as a leader of the organization

<https://github.com/comp423-24s/csxl-final-team-a3/blob/8c6bd2803d73f1edc2c71326b0a8e97ad7ed0609/backend/services/member.py#L462-L496>

-   update: this function updates the selected member's information when you update the 'title' of the member 

<https://github.com/comp423-24s/csxl-final-team-a3/blob/8c6bd2803d73f1edc2c71326b0a8e97ad7ed0609/backend/services/member.py#L498-L545>

# APIs:

The following APIs were used to create, read, update, and delete members of an organization:

-   get_member_details: gets the approved members from an organization

<https://github.com/comp423-24s/csxl-final-team-a3/blob/8c6bd2803d73f1edc2c71326b0a8e97ad7ed0609/backend/api/members.py#L27-L52>

-   add_member: posts a member request to the member database

<https://github.com/comp423-24s/csxl-final-team-a3/blob/8c6bd2803d73f1edc2c71326b0a8e97ad7ed0609/backend/api/members.py#L227-L254>

-   approve_member: puts the approvalStatus field from False to True, in order to approve a user's membership into an organization

<https://github.com/comp423-24s/csxl-final-team-a3/blob/8c6bd2803d73f1edc2c71326b0a8e97ad7ed0609/backend/api/members.py#L143-L168>

-   get_approved_member_details: gets the MemberDetails of the approved members of the organization 

<https://github.com/comp423-24s/csxl-final-team-a3/blob/8c6bd2803d73f1edc2c71326b0a8e97ad7ed0609/backend/api/members.py#L85-L112>

-   get_pending_member_details: gets the MemberDetails of the members that have requested membership but haven't been approved yet, for example approvalStatus of 'False'

<https://github.com/comp423-24s/csxl-final-team-a3/blob/8c6bd2803d73f1edc2c71326b0a8e97ad7ed0609/backend/api/members.py#L114-L141>

-   delete_member: deletes the selected member from the organization

<https://github.com/comp423-24s/csxl-final-team-a3/blob/8c6bd2803d73f1edc2c71326b0a8e97ad7ed0609/backend/api/members.py#L256-L285>

-   admin_status: this function makes (puts) the selected member an admin of the organization

<https://github.com/comp423-24s/csxl-final-team-a3/blob/8c6bd2803d73f1edc2c71326b0a8e97ad7ed0609/backend/api/members.py#L171-L197>

-   remove_admin: this function removes (puts) the admin privileges of the member 

<https://github.com/comp423-24s/csxl-final-team-a3/blob/8c6bd2803d73f1edc2c71326b0a8e97ad7ed0609/backend/api/members.py#L199-L224>

-   get_member_by_id: this function fetches (gets) the member of an organization based on their member

<https://github.com/comp423-24s/csxl-final-team-a3/blob/8c6bd2803d73f1edc2c71326b0a8e97ad7ed0609/backend/api/members.py#L56-L83>

-   make_leader: this function makes the selected user a leader of the organization

<https://github.com/comp423-24s/csxl-final-team-a3/blob/8c6bd2803d73f1edc2c71326b0a8e97ad7ed0609/backend/api/members.py#L287-L312>

-   get_leader_details: this function retrieves the details of the leader of an organization

<https://github.com/comp423-24s/csxl-final-team-a3/blob/8c6bd2803d73f1edc2c71326b0a8e97ad7ed0609/backend/api/members.py#L315-L340>

-   get_member_details_by_term: this function retrieves (gets)  the details of the member of an organization based on the term

-   remove_leader: this function removes (puts) the selected member as a leader of the organization

<https://github.com/comp423-24s/csxl-final-team-a3/blob/8c6bd2803d73f1edc2c71326b0a8e97ad7ed0609/backend/api/members.py#L343-L368>

-   update_member: this function updates the selected member's information when you update the 'title' of the member 

<https://github.com/comp423-24s/csxl-final-team-a3/blob/8c6bd2803d73f1edc2c71326b0a8e97ad7ed0609/backend/api/members.py#L374>

# Testing:

<https://github.com/comp423-24s/csxl-final-team-a3/blob/stage/backend/test/services/member_test.py>

# Future Developers:

-   We would like to implement features that would allow organizations to create member only events that can not be viewed by non-members

-   We would like to implement features that allow organizations to post member specific news and announcements

-   We would like to implement features that allow organizations to integrate and implement applications for applications-based memberships on the CSXL site.

You will need to test in two views (one as Rhona Root initially, then one as yourself)