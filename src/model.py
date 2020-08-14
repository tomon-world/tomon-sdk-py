from dataclasses import dataclass, field
from typing import List, Optional, ClassVar, Type

import marshmallow_dataclass
import marshmallow.validate
from marshmallow import Schema


# @dataclass
# class User:
#     pass
#
#
# @dataclass
# class Guild:
#     pass
#
#
# @dataclass
# class GuildPosition:
#     pass
#
#
# @dataclass
# class Overwrite:
#     pass
#
#
# @dataclass
# class Channel:
#     pass
#
#
# @dataclass
# class ChannelPosition:
#     pass
#
#
# @dataclass
# class Role:
#     pass
#
#
# @dataclass
# class RolePosition:
#     pass
#
#
# @dataclass
# class Message:
#     pass
#
#
# @dataclass
# class GuildMember:
#     pass
#
#
# @dataclass
# class Emoji:
#     pass
#
#
# @dataclass
# class MessageReaction:
#     pass
#
#
# @dataclass
# class MessageReactionRemoveAll:
#     pass
#
#
# @dataclass
# class VoiceState:
#     pass
#
#
# @dataclass
# class Presence:
#     pass
#
#
# @dataclass
# class PartialPresence:
#     pass
#
#
# @dataclass
# class Ready:
#     pass
#
#
# @dataclass
# class Identity:
#     pass
#
#
# @dataclass
# class Logout:
#     pass
#
#
# @dataclass
# class Typing:
#     pass
#
#
# @dataclass
# class UserGuildSettings:
#     pass
#
#
# @dataclass
# class Stamp:
#     pass
#
#
# @dataclass
# class StampPack:
#     pass
#
#
# @dataclass
# class Embed:
#     pass
#
#
# @dataclass
# class MessageForward:
#     pass
#
#
# @dataclass
# class ForwardThumb:
#     pass
#
#
# @dataclass
# class ForwardMessage:
#     pass
#
#
# @dataclass
# class Forward:
#     pass
#
# 用户
@dataclass
class User:
    id: int = field()
    username: str = field()
    discriminator: str = field()
    avatar: str = field()
    avatar_url: str = field()
    name: str = field()
    type: int = field()


# 公会
@dataclass
class Guild:
    id: int = field()
    name: str = field()
    icon: str = field()
    icon_url: str = field()
    position: int = field()
    created_at: str = field()
    joined_at: str = field()
    owner_id: int = field()
    system_channel_id: int = field()
    system_channel_flags: int = field()
    background: str = field()
    background_url: str = field()
    background_props: str = field()
    members: List[GuildMember] = field()


@dataclass
class GuildMember:
    user: User = field()
    guild_id: int = field()
    nick: str = field()
    roles: List[int] = field()
    joined_at: str = field()
    deaf: bool = field()
    mute: bool = field()
    silence_expired: str = field()


@dataclass
class UserTyping:
    user_id: int = field()
    channel_id: int = field()
    member: GuildMember = field()
    timestamp: str = field()


@dataclass
class Presence:
    user: User = field()
    status: str = field()
