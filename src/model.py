from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field
from typing import List, Optional, ClassVar, Type

import marshmallow_dataclass
import marshmallow.validate
from marshmallow import Schema


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
    channels: List[Channel] = field(default_factory=list)
    roles: List[Role] = field(default_factory=list)
    emojis: List[Emoji] = field(default_factory=list)
    members: List[GuildMember] = field(default_factory=list)
    voice_states: List[VoiceState] = field(default_factory=list)
    presences: List[PartialPresence] = field(default_factory=list)


@dataclass
class GuildPosition:
    @dataclass
    class Position:
        id: int = field()
        position: int = field()

    positions: List[Position] = field(default_factory=list)


@dataclass
class Overwrite:
    id: int = field()
    type: str = field()
    allow: int = field()
    deny: int = field()


@dataclass
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
    recipients: List[User] = field(default_factory=list)
    permission_overwrites: List[Overwrite] = field(default_factory=list)


@dataclass
class ChannelPosition:
    @dataclass
    class Position:
        id: int = field()
        position: int = field()
        parent_id: str = field()

    guild_id: int = field()
    positions: List[Position] = field(default_factory=list)


@dataclass
class Role:
    id: str = field()
    guild_id: str = field()
    name: str = field()
    permissions: int = field()
    color: int = field()
    position: int = field()
    hoist: bool = field()
    mentionable: bool = field()


@dataclass
class RolePosition:
    @dataclass
    class Position:
        id: int = field()
        position: int = field()

    guild_id: int = field()
    positions: List[Position] = field(default_factory=list)


@dataclass
class Message:
    @dataclass
    class Member:
        nick: str = field()
        roles: List[int] = field()

    @dataclass
    class Attachment:
        id: int = field()
        filename: int = field()
        hash: str = field()
        type: str = field()
        size: str = field()
        width: int = field()
        height: int = field()
        url: str = field()

    id: int = field()
    channel_id: int = field()
    type: int = field()
    timestamp: str = field()
    nonce: int = field()
    content: str = field()
    author: User = field()
    member: Member = field()
    reply: Message = field()
    forward: MessageForward = field()
    pinned: bool = field()
    edited_timestamp: str = field()
    attachments: List[Attachment] = field(default_factory=list)
    mentions: List[User] = field(default_factory=list)
    stamps: List[Stamp] = field(default_factory=list)
    embeds: List[Embed] = field(default_factory=list)


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
class Emoji:
    id: int = field()
    guild_id: int = field()
    name: str = field()
    user: User = field()
    img: str = field()
    img_url: str = field()


@dataclass
class MEmoji:
    id: int = field()
    name: str = field()


@dataclass
class MessageReaction:
    user_id: int = field()
    channel_id: int = field()
    message_id: int = field()
    guild_id: int = field()
    emoji: MEmoji = field()


@dataclass
class MessageReactionRemoveAll:
    channel_id: int = field()
    message_id: int = field()
    guild_id: int = field()


@dataclass
class VoiceState:
    user_id: int = field()
    channel_id: int = field()
    guild_id: int = field()
    voice: int = field()
    session_id: str = field()
    user: User = field()
    self_deaf: bool = field()
    self_mute: bool = field()


@dataclass
class Presence:
    user: User = field()
    status: str = field()


@dataclass
class PartialPresence:
    user_id: int = field()
    status: str = field()


@dataclass
class Ready:
    @dataclass
    class Channel:
        id: int = field()
        type: int = field()
        permission_overwrites: List[Overwrite] = field(default_factory=list)

    @dataclass
    class DMChannel:
        id: int = field()
        type: int = field()
        visible: bool = field()

    @dataclass
    class Role:
        id: int = field()
        permissions: int = field()
        position: int = field()

    @dataclass
    class Guild:
        id: int = dataclasses.field()
        owner_id: int = dataclasses.field()
        member_roles: List[int] = dataclasses.field()
        channels: List[Channel] = field(default_factory=list)
        roles: List[Role] = field(default_factory=list)

    # user: 'User' = field()
    guilds: List[Guild] = field(default_factory=list)
    channels: List[DMChannel] = field(default_factory=list)


@dataclass
class Identity:
    guilds: List[Guild] = field(default_factory=list)
    guild_settings: List[UserGuildSettings] = field(default_factory=list)
    dm_channels: List[Channel] = field(default_factory=list)
    stamp_packs: List[StampPack] = field(default_factory=list)


@dataclass
class Logout:
    userId: int = field()
    sessionId: str = field()


@dataclass
class Typing:
    user_id: int = field()
    channel_id: int = field()
    member: GuildMember = field()
    timestamp: str = field()


@dataclass
class UserGuildSettings:
    @dataclass
    class ChannelOverride:
        channel_id: int = field()
        message_notifications: int = field()
        muted: bool = field()

    guild_id: int = field()
    message_notifications: int = field()
    muted: bool = field()
    channel_overrides: ChannelOverride = field()
    suppress_everyone: bool = field()


@dataclass
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


@dataclass
class StampPack:
    id: int = field()
    name: str = field()
    type: int = field()
    author_id: int = field()
    updated_at: str = field()
    stamps: List[Stamp] = field(default_factory=list)


@dataclass
class Embed:
    @dataclass
    class Author:
        author_name: str = field()
        author_url: str = field()

    @dataclass
    class Provider:
        provider_name: str = field()
        provider_url: str = field()

    @dataclass
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


@dataclass
class MessageForward:
    @dataclass
    class Guild:
        id: int = field()
        name: str = field()

    @dataclass
    class Channel:
        id: int = field()
        name: str = field()

    id: int = field()
    guild: 'Guild' = field()
    channel: 'Channel' = field()
    thumb: List[ForwardThumb] = field(default_factory=list)


@dataclass
class ForwardThumb:
    @dataclass
    class Author:
        id: int = field()
        avatar: str = field()
        type: int = field()
        dname: str = field()

    @dataclass
    class Attachment:
        hash: str = field()
        type: str = field()

    @dataclass
    class Stamp:
        hash: str = field()
        animated: bool = field()

    id: int = field()
    content: str = field()
    author: Author = field()
    attachment: Attachment = field()
    stamp: Stamp = field()


@dataclass
class ForwardMessage:
    @dataclass
    class Author:
        id: int = field()
        avatar: str = field()
        type: int = field()
        dname: str = field()

    @dataclass
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
    reply: 'Message' = field()
    timestamp: str = field()
    stamps: List[Stamp] = field(default_factory=list)
    attachments: List[Attachment] = field(default_factory=list)


@dataclass
class Forward:
    @dataclass
    class Guild:
        id: int = field()
        name: str = field()

    @dataclass
    class Channel:
        id: int = field()
        name: str = field()

    id: int = field()
    content: str = field()
    guild: Guild = field()
    channel: Channel = field()
    messages: List[ForwardMessage] = field(default_factory=list)
    thumb: List[ForwardThumb] = field(default_factory=list)
