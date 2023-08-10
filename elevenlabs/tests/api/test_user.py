import pytest
import asyncio


def test_user():
    from elevenlabs import Subscription, User

    # Test that we can get current user
    user = User.from_api()
    assert isinstance(user, User)
    assert isinstance(user.subscription, Subscription)


@pytest.mark.asyncio
async def test_auser():
    from elevenlabs import Subscription, User

    # Test that we can get current user
    user = await User.afrom_api()
    assert isinstance(user, User)
    assert isinstance(user.subscription, Subscription)


@pytest.mark.asyncio
async def test_gather_user():
    from elevenlabs import Subscription, User

    # Test that we can get current user
    users = await asyncio.gather(*[User.afrom_api() for _ in range(10)])
    for user in users:
        assert isinstance(user, User)
        assert isinstance(user.subscription, Subscription)
