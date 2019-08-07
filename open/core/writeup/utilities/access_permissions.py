from open.core.writeup.constants import PromptShareStates, StaffVerifiedShareStates


def user_can_read_prompt_instance(user, prompt):
    if prompt.user == user:
        return True

    # if this is marked as some type of bad content, no one should see
    if prompt.staff_verified_share_state in [
        StaffVerifiedShareStates.VERIFIED_FAIL,
        StaffVerifiedShareStates.UNVERIFIED_ISSUE_MULTIPLE,
    ]:
        return False

    if prompt.share_state in [
        PromptShareStates.PUBLISHED,
        PromptShareStates.PUBLISHED_LINK_ACCESS_ONLY,
    ]:
        return True

    return False
