from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field
from typing import List, Optional, ClassVar, Type

import marshmallow_dataclass
import marshmallow.validate
from marshmallow import Schema


# @dataclasses.dataclass()
# class User:
#     pass
#
#
# @dataclasses.dataclass()
# class Guild:
#     pass
#
#
# @dataclasses.dataclass()
# class GuildPosition:
#     pass
#
#
# @dataclasses.dataclass()
# class Overwrite:
#     pass
#
#
# @dataclasses.dataclass()
# class Channel:
#     pass
#
#
# @dataclasses.dataclass()
# class ChannelPosition:
#     pass
#
#
# @dataclasses.dataclass()
# class Role:
#     pass
#
#
# @dataclasses.dataclass()
# class RolePosition:
#     pass
#
#
# @dataclasses.dataclass()
# class Message:
#     pass
#
#
# @dataclasses.dataclass()
# class GuildMember:
#     pass
#
#
# @dataclasses.dataclass()
# class Emoji:
#     pass
#
#
# @dataclasses.dataclass()
# class MessageReaction:
#     pass
#
#
# @dataclasses.dataclass()
# class MessageReactionRemoveAll:
#     pass
#
#
# @dataclasses.dataclass()
# class VoiceState:
#     pass
#
#
# @dataclasses.dataclass()
# class Presence:
#     pass
#
#
# @dataclasses.dataclass()
# class PartialPresence:
#     pass
#
#
# @dataclasses.dataclass()
# class Ready:
#     pass
#
#
# @dataclasses.dataclass()
# class Identity:
#     pass
#
#
# @dataclasses.dataclass()
# class Logout:
#     pass
#
#
# @dataclasses.dataclass()
# class Typing:
#     pass
#
#
# @dataclasses.dataclass()
# class UserGuildSettings:
#     pass
#
#
# @dataclasses.dataclass()
# class Stamp:
#     pass
#
#
# @dataclasses.dataclass()
# class StampPack:
#     pass
#
#
# @dataclasses.dataclass()
# class Embed:
#     pass
#
#
# @dataclasses.dataclass()
# class MessageForward:
#     pass
#
#
# @dataclasses.dataclass()
# class ForwardThumb:
#     pass
#
#
# @dataclasses.dataclass()
# class ForwardMessage:
#     pass
#
#
# @dataclasses.dataclass()
# class Forward:
#     pass
#
# 用户
@dataclasses.dataclass()
class User:
    id: int = field()
    username: str = field()
    discriminator: str = field()
    avatar: str = field()
    avatar_url: str = field()
    name: str = field()
    type: int = field()


# 公会
@dataclasses.dataclass()
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
    channels: List['Channel'] = field()
    roles: List['Role'] = field()
    emojis: List['Emoji'] = field()
    members: List['GuildMember'] = field()
    voice_states: List['VoiceState'] = field()
    presences: List['PartialPresence'] = field()


@dataclasses.dataclass()
class GPosition:
    id: int = field()
    position: int = field()


@dataclasses.dataclass()
class GuildPosition:
    positions: List['GPosition'] = field()


@dataclasses.dataclass()
class Overwrite:
    id: int = field()
    type: str = field()
    allow: int = field()
    deny: int = field()


@dataclasses.dataclass()
class Channel:
    id: int = field()
    name: str = field()
    type: int = field()
    guild_id: int = field()
    position: int = field()
    topic: str = field()
    last_message_id: int = field()
    parent_id: int = field()
    ack_message_id: int = field()
    default_message_notifications: int = field()
    bitrate: int = field()
    user_limit: int = field()
    last_pin_timestamp: str = field()
    unread_count: int = field()
    recipients: List[User] = dataclasses.field(default_factory=lambda: [])
    permission_overwrites: List[Overwrite] = dataclasses.field(default_factory=lambda: [])


@dataclasses.dataclass()
class CPosition:
    id: int = field()
    position: int = field()
    parent_id: str = field()


@dataclasses.dataclass()
class ChannelPosition:
    guild_id: int = field()
    positions: List['CPosition'] = field()


@dataclasses.dataclass()
class Role:
    id: str = field()
    guild_id: str = field()
    name: str = field()
    permissions: int = field()
    color: int = field()
    position: int = field()
    hoist: bool = field()
    mentionable: bool = field()


@dataclasses.dataclass()
class RPosition:
    id: int = field()
    position: int = field()


@dataclasses.dataclass()
class RolePosition:
    guild_id: int = field()
    positions: List['RPosition'] = field()


@dataclasses.dataclass()
class MMember:
    nick: str = field()
    roles: List[int] = field()


@dataclasses.dataclass()
class MAttachment:
    id: int = field()
    filename: int = field()
    hash: str = field()
    type: str = field()
    size: str = field()
    width: int = field()
    height: int = field()
    url: str = field()


@dataclasses.dataclass()
class Message:
    id: int = field()
    channel_id: int = field()
    type: int = field()
    timestamp: str = field()
    nonce: int = field()
    content: str = field()
    author: User = field()
    member: 'MMember' = field()
    attachments: List['MAttachment'] = field()
    mentions: List['User'] = field()
    stamps: List['Stamp'] = field()
    reply: 'Message' = field()
    forward: 'MessageForward' = field()
    pinned: bool = field()
    edited_timestamp: str = field()
    embeds: List['Embed'] = field()


@dataclasses.dataclass()
class GuildMember:
    user: User = field()
    guild_id: int = field()
    nick: str = field()
    roles: List[int] = field()
    joined_at: str = field()
    deaf: bool = field()
    mute: bool = field()
    silence_expired: str = field()


@dataclasses.dataclass()
class Emoji:
    id: int = field()
    guild_id: int = field()
    name: str = field()
    user: User = field()
    img: str = field()
    img_url: str = field()


@dataclasses.dataclass()
class MEmoji:
    id: int = field()
    name: str = field()


@dataclasses.dataclass()
class MessageReaction:
    user_id: int = field()
    channel_id: int = field()
    message_id: int = field()
    guild_id: int = field()
    emoji: 'MEmoji' = field()


@dataclasses.dataclass()
class MessageReactionRemoveAll:
    channel_id: int = field()
    message_id: int = field()
    guild_id: int = field()


@dataclasses.dataclass()
class VoiceState:
    user_id: int = field()
    channel_id: int = field()
    guild_id: int = field()
    voice: int = field()
    session_id: str = field()
    user: 'User' = field()
    self_deaf: bool = field()
    self_mute: bool = field()


@dataclasses.dataclass()
class Presence:
    user: 'User' = field()
    status: str = field()


@dataclasses.dataclass()
class PartialPresence:
    user_id: int = field()
    status: str = field()


@dataclasses.dataclass()
class Ready:
    @dataclasses.dataclass()
    class Channel:
        id: int = field()
        type: int = field()
        permission_overwrites: List[Overwrite] = dataclasses.field(default_factory=lambda: [])

    @dataclasses.dataclass()
    class DMChannel:
        id: int = field()
        type: int = field()
        visible: bool = field()

    @dataclasses.dataclass()
    class Role:
        id: int = field()
        permissions: int = field()
        position: int = field()

    @dataclasses.dataclass()
    class Guild:
        id: int = dataclasses.field()
        owner_id: int = dataclasses.field()
        channels: List[Channel] = dataclasses.field(default_factory=lambda: [])
        roles: List[Role] = dataclasses.field(default_factory=lambda: [])
        member_roles: List[int] = dataclasses.field(default_factory=lambda: [])

    # user: 'User' = field()
    guilds: List[Guild] = dataclasses.field(default_factory=lambda: [])
    channels: List[DMChannel] = dataclasses.field(default_factory=lambda: [])


@dataclasses.dataclass()
class Identity:
    guilds: List['Guild'] = field()
    guild_settings: List['UserGuildSettings'] = field()
    dm_channels: List['Channel'] = field()
    stamp_packs: List['StampPack'] = field()


@dataclasses.dataclass()
class Logout:
    userId: int = field()
    sessionId: str = field()


@dataclasses.dataclass()
class Typing:
    user_id: int = field()
    channel_id: int = field()
    member: 'GuildMember' = field()
    timestamp: str = field()


@dataclasses.dataclass()
class UserGuildSettings:
    @dataclasses.dataclass()
    class ChannelOverride:
        channel_id: int = field()
        message_notifications: int = field()
        muted: bool = field()

    guild_id: int = field()
    message_notifications: int = field()
    muted: bool = field()
    channel_overrides: 'ChannelOverride' = field()
    suppress_everyone: bool = field()


@dataclasses.dataclass()
class Stamp:
    id: int = field()
    alias: str = field()
    author_id: int = field()
    pack_id: int = field()
    position: int = field()
    hash: str = field()
    animated: bool = field()
    width: int = field()
    height: int = field()
    updated_at: str = field()


@dataclasses.dataclass()
class StampPack:
    id: int = field()
    name: str = field()
    type: int = field()
    author_id: int = field()
    stamps: List['Stamp'] = field()
    updated_at: str = field()


@dataclasses.dataclass()
class Embed:
    @dataclasses.dataclass()
    class Author:
        author_name: str = field()
        author_url: str = field()

    @dataclasses.dataclass()
    class Provider:
        provider_name: str = field()
        provider_url: str = field()

    @dataclasses.dataclass()
    class Thumbnail:
        thumbnail_url: str = field()
        thumbnail_height: int = field()
        thumbnail_width: int = field()
        external_url: str = field()

    id: int = field()
    type: str = field()
    title: str = field()
    url: str = field()
    description: str = field()
    height: int = field()
    width: int = field()
    author: Author = field()
    provider: Provider = field()
    thumbnail: Thumbnail = field()


@dataclasses.dataclass()
class MessageForward:
    @dataclasses.dataclass()
    class Guild:
        id: int = field()
        name: str = field()

    @dataclasses.dataclass()
    class Channel:
        id: int = field()
        name: str = field()

    id: int = field()
    guild: 'Guild' = field()
    channel: 'Channel' = field()
    thumb: List['ForwardThumb'] = field()


@dataclasses.dataclass()
class ForwardThumb:
    @dataclasses.dataclass()
    class Author:
        id: int = field()
        avatar: str = field()
        type: int = field()
        dname: str = field()

    @dataclasses.dataclass()
    class Attachment:
        hash: str = field()
        type: str = field()

    @dataclasses.dataclass()
    class Stamp:
        hash: str = field()
        animated: bool = field()

    id: int = field()
    content: str = field()
    author: Author = field()
    attachment: Attachment = field()
    stamp: Stamp = field()


@dataclasses.dataclass()
class ForwardMessage:
    @dataclasses.dataclass()
    class Author:
        id: int = field()
        avatar: str = field()
        type: int = field()
        dname: str = field()

    @dataclasses.dataclass()
    class Attachment:
        id: int = field()
        filename: str = field()
        hash: str = field()
        type: str = field()
        size: int = field()
        width: int = field()
        height: int = field()
        url: str = field()

    id: int = field()
    content: str = field()
    stamps: List['Stamp'] = field()
    attachments: List['Attachment'] = field()
    reply: 'Message' = field()
    timestamp: str = field()


@dataclasses.dataclass()
class Forward:
    @dataclasses.dataclass()
    class Guild:
        id: int = field()
        name: str = field()

    @dataclasses.dataclass()
    class Channel:
        id: int = field()
        name: str = field()

    id: int = field()
    content: str = field()
    guild: Guild = field()
    channel: Channel = field()
    messages: List['ForwardMessage'] = field()
    thumb: List['ForwardThumb'] = field()
