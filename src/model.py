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
    channels: List['Channel'] = field()
    roles: List['Role'] = field()
    emojis: List['Emoji'] = field()
    members: List['GuildMember'] = field()
    voice_states: List['VoiceState'] = field()
    presences: List['PartialPresence'] = field()


@dataclass
class GPosition:
    id: int = field()
    position: int = field()


@dataclass
class GuildPosition:
    positions: List['GPosition'] = field()


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
    permission_overwrites: List['Overwrite'] = field()
    ack_message_id: int = field()
    default_message_notifications: int = field()
    bitrate: int = field()
    user_limit: int = field()
    recipients: List['User'] = field()
    last_pin_timestamp: str = field()
    unread_count: int = field()


@dataclass
class CPosition:
    id: int = field()
    position: int = field()
    parent_id: str = field()


@dataclass
class ChannelPosition:
    guild_id: int = field()
    positions: List['CPosition'] = field()


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
class RPosition:
    id: int = field()
    position: int = field()


@dataclass
class RolePosition:
    guild_id: int = field()
    positions: List['RPosition'] = field()


@dataclass
class MMember:
    nick: str = field()
    roles: List[int] = field()


@dataclass
class MAttachment:
    id: int = field()
    filename: int = field()
    hash: str = field()
    type: str = field()
    size: str = field()
    width: int = field()
    height: int = field()
    url: str = field()


@dataclass
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
    emoji: 'MEmoji' = field()


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
    user: 'User' = field()
    self_deaf: bool = field()
    self_mute: bool = field()


@dataclass
class Presence:
    user: 'User' = field()
    status: str = field()


@dataclass
class PartialPresence:
    user_id: int = field()
    status: str = field()


@dataclass
class RChannel:
    id: int = field()
    type: int = field()
    permission_overwrites: List['Overwrite'] = field()


@dataclass
class RDMChannel:
    id: int = field()
    type: int = field()
    visible: bool = field()


@dataclass
class RRole:
    id: int = field()
    permissions: int = field()
    position: int = field()


@dataclass
class RGuild:
    id: int = field()
    channels: List['RChannel'] = field()
    roles: List['RRole'] = field()
    member_roles: List[int] = field()
    owner_id: int = field()


@dataclass
class Ready:
    user: 'User' = field()
    guilds: List['RGuild'] = field()
    channels: List['RDMChannel'] = field()


@dataclass
class Identity:
    guilds: List['Guild'] = field()
    guild_settings: List['UserGuildSettings'] = field()
    dm_channels: List['Channel'] = field()
    stamp_packs: List['StampPack'] = field()


@dataclass
class Logout:
    userId: int = field()
    sessionId: str = field()


@dataclass
class Typing:
    user_id: int = field()
    channel_id: int = field()
    member: 'GuildMember' = field()
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
    channel_overrides: 'ChannelOverride' = field()
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
    stamps: List['Stamp'] = field()
    updated_at: str = field()


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
    thumb: List['ForwardThumb'] = field()


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
    stamps: List['Stamp'] = field()
    attachments: List['Attachment'] = field()
    reply: 'Message' = field()
    timestamp: str = field()


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
    messages: List['ForwardMessage'] = field()
    thumb: List['ForwardThumb'] = field()
