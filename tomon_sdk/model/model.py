from __future__ import annotations
from typing import List

from marshmallow import Schema, fields


class User(Schema):
    id: int = fields.Int()
    username: str = fields.Str()
    discriminator: str = fields.Str()
    avatar: str = fields.Str()
    avatar_url: str = fields.Str()
    name: str = fields.Str()
    type: int = fields.Int()


class Emoji(Schema):
    id: int = fields.Int()
    guild_id: int = fields.Int()
    name: str = fields.Str()
    user: User = fields.Nested(User)
    img: str = fields.Str()
    img_url: str = fields.Str()


class GPosition(Schema):
    id: int = fields.Int()
    position: int = fields.Int()


class GuildPosition(Schema):
    positions: List[GPosition] = fields.List(fields.Nested(GPosition))


class Overwrite(Schema):
    id: int = fields.Int()
    type: str = fields.Str()
    allow: int = fields.Int()
    deny: int = fields.Int()


class VoiceState(Schema):
    user_id: int = fields.Int()
    channel_id: int = fields.Int()
    guild_id: int = fields.Int()
    voice: int = fields.Int()
    session_id: str = fields.Str()
    user: 'User' = fields.Nested(User)
    self_deaf: bool = fields.Bool()
    self_mute: bool = fields.Bool()


class Role(Schema):
    id: str = fields.Str()
    guild_id: str = fields.Str()
    name: str = fields.Str()
    permissions: int = fields.Int()
    color: int = fields.Int()
    position: int = fields.Int()
    hoist: bool = fields.Bool()
    mentionable: bool = fields.Bool()


class PartialPresence(Schema):
    user_id: int = fields.Int()
    status: str = fields.Str()


class Channel(Schema):
    id: int = fields.Int()
    name: str = fields.Str()
    type: int = fields.Int()
    guild_id: int = fields.Int()
    position: int = fields.Int()
    topic: str = fields.Str()
    last_message_id: int = fields.Int()
    parent_id: int = fields.Int()
    ack_message_id: int = fields.Int()
    default_message_notifications: int = fields.Int()
    bitrate: int = fields.Int()
    user_limit: int = fields.Int()
    last_pin_timestamp: str = fields.Str()
    unread_count: int = fields.Int()
    recipients: List[User] = fields.List(fields.Nested(User))
    permission_overwrites: List[Overwrite] = fields.List(fields.Nested(Overwrite))


class GuildMember(Schema):
    user: User = fields.Nested(User)
    guild_id: int = fields.Int()
    nick: str = fields.Str()
    roles: List[int] = fields.List(fields.Int)
    joined_at: str = fields.Str()
    deaf: bool = fields.Bool
    mute: bool = fields.Bool
    silence_expired: str = fields.Str()


class Guild(Schema):
    id: int = fields.Int()
    name: str = fields.Str()
    icon: str = fields.Str()
    icon_url: str = fields.Str()
    position: int = fields.Int()
    created_at: str = fields.Str()
    joined_at: str = fields.Str()
    owner_id: int = fields.Int()
    system_channel_id: int = fields.Int()
    system_channel_flags: int = fields.Int()
    background: str = fields.Str()
    background_url: str = fields.Str()
    background_props: str = fields.Str()
    channels: List['Channel'] = fields.List(fields.Nested(Channel))
    roles: List['Role'] = fields.List(fields.Nested(Role))
    emojis: List['Emoji'] = fields.List(fields.Nested(Emoji))
    members: List['GuildMember'] = fields.List(fields.Nested(GuildMember))
    voice_states: List['VoiceState'] = fields.List(fields.Nested(VoiceState))
    presences: List['PartialPresence'] = fields.List(fields.Nested(PartialPresence))


class CPosition(Schema):
    id: int = fields.Int()
    position: int = fields.Int()
    parent_id: str = fields.Str()


class ChannelPosition(Schema):
    guild_id: int = fields.Int()
    positions: List['CPosition'] = fields.List(fields.Nested(CPosition))


class Stamp(Schema):
    id: int = fields.Int()
    alias: str = fields.Str()
    author_id: int = fields.Int()
    pack_id: int = fields.Int()
    position: int = fields.Int()
    hash: str = fields.Str()
    animated: bool = fields.Bool
    width: int = fields.Int()
    height: int = fields.Int()
    updated_at: str = fields.Str()


class StampPack(Schema):
    id: int = fields.Int()
    name: str = fields.Str()
    type: int = fields.Int()
    author_id: int = fields.Int()
    stamps: List['Stamp'] = fields.List(fields.Nested(Stamp))
    updated_at: str = fields.Str()


class ForwardThumb(Schema):
    class Author(Schema):
        id: int = fields.Int()
        avatar: str = fields.Str()
        type: int = fields.Int()
        dname: str = fields.Str()

    class Attachment(Schema):
        hash: str = fields.Str()
        type: str = fields.Str()

    class Stamp(Schema):
        hash: str = fields.Str()
        animated: bool = fields.Bool()

    id: int = fields.Int()
    content: str = fields.Str()
    author: Author = fields.Nested(Author)
    attachment: Attachment = fields.Nested(Attachment)
    stamp: Stamp = fields.Nested(Stamp)


class MessageForward(Schema):
    class Guild(Schema):
        id: int = fields.Int()
        name: str = fields.Str()

    class Channel(Schema):
        id: int = fields.Int()
        name: str = fields.Str()

    id: int = fields.Int()
    guild: 'Guild' = fields.Nested(Guild)
    channel: 'Channel' = fields.Nested(Channel)
    thumb: List['ForwardThumb'] = fields.List(fields.Nested(ForwardThumb))


class Embed(Schema):
    class Author(Schema):
        author_name: str = fields.Str()
        author_url: str = fields.Str()

    class Provider(Schema):
        provider_name: str = fields.Str()
        provider_url: str = fields.Str()

    class Thumbnail(Schema):
        thumbnail_url: str = fields.Str()
        thumbnail_height: int = fields.Int()
        thumbnail_width: int = fields.Int()
        external_url: str = fields.Str()

    id: int = fields.Int()
    type: str = fields.Str()
    title: str = fields.Str()
    url: str = fields.Str()
    description: str = fields.Str()
    height: int = fields.Int()
    width: int = fields.Int()
    author: Author = fields.Nested(Author)
    provider: Provider = fields.Nested(Provider)
    thumbnail: Thumbnail = fields.Nested(Thumbnail)


class RPosition(Schema):
    id: int = fields.Int()
    position: int = fields.Int()


class RolePosition(Schema):
    guild_id: int = fields.Int()
    positions: List['RPosition'] = fields.List(fields.Nested(RPosition))


class MMember(Schema):
    nick: str = fields.Str()
    roles: List[int] = fields.List(fields.Int)


class MAttachment(Schema):
    id: int = fields.Int()
    filename: int = fields.Int()
    hash: str = fields.Str()
    type: str = fields.Str()
    size: str = fields.Str()
    width: int = fields.Int()
    height: int = fields.Int()
    url: str = fields.Str()


class Message(Schema):
    id: int = fields.Int()
    channel_id: int = fields.Int()
    type: int = fields.Int()
    timestamp: str = fields.Str()
    nonce: int = fields.Int()
    content: str = fields.Str()
    author: User = fields.Nested(User())
    member: 'MMember' = fields.Nested(MMember())
    attachments: List['MAttachment'] = fields.List(fields.Nested(MAttachment))
    mentions: List['User'] = fields.List(fields.Nested(User))
    stamps: List['Stamp'] = fields.List(fields.Nested(Stamp))
    reply: 'Message' = fields.Nested('Message')
    forward: 'MessageForward' = fields.Nested(MessageForward)
    pinned: bool = fields.Bool()
    edited_timestamp: str = fields.Str()
    embeds: List['Embed'] = fields.List(fields.Nested(Embed))


class MEmoji(Schema):
    id: int = fields.Int()
    name: str = fields.Str()


class MessageReaction(Schema):
    user_id: int = fields.Int()
    channel_id: int = fields.Int()
    message_id: int = fields.Int()
    guild_id: int = fields.Int()
    emoji: 'MEmoji' = fields.Nested(MEmoji)


class MessageReactionRemoveAll(Schema):
    channel_id: int = fields.Int()
    message_id: int = fields.Int()
    guild_id: int = fields.Int()


class Presence(Schema):
    user: 'User' = fields.Nested(User)
    status: str = fields.Str()


class Ready(Schema):
    class Channel(Schema):
        id: int = fields.Int()
        type: int = fields.Int()
        permission_overwrites: List[Overwrite] = fields.List(fields.Nested(Overwrite))

    class DMChannel(Schema):
        id: int = fields.Int()
        type: int = fields.Int()
        visible: bool = fields.Bool()

    class Role(Schema):
        id: int = fields.Int()
        permissions: int = fields.Int()
        position: int = fields.Int()

    class Guild(Schema):
        id: int = fields.Int()
        owner_id: int = fields.Int()
        channels: List[Channel] = fields.List(fields.Nested(Channel))
        roles: List[Role] = fields.List(fields.Nested(Role))
        member_roles: List[int] = fields.List(fields.Int)

    # user: 'User' = field()
    guilds: List[Guild] = fields.List(fields.Nested(Guild))
    channels: List[DMChannel] = fields.List(fields.Nested(DMChannel))


class UserGuildSettings(Schema):
    class ChannelOverride(Schema):
        channel_id: int = fields.Int()
        message_notifications: int = fields.Int()
        muted: bool = fields.Bool

    guild_id: int = fields.Int()
    message_notifications: int = fields.Int()
    muted: bool = fields.Bool
    channel_overrides: 'ChannelOverride' = fields.Nested(ChannelOverride)
    suppress_everyone: bool = fields.Bool


class Identity(Schema):
    guilds: List['Guild'] = fields.List(fields.Nested(Guild))
    guild_settings: List['UserGuildSettings'] = fields.List(fields.Nested(UserGuildSettings))
    dm_channels: List['Channel'] = fields.List(fields.Nested(Channel))
    stamp_packs: List['StampPack'] = fields.List(fields.Nested(StampPack))


class Logout(Schema):
    userId: int = fields.Int()
    sessionId: str = fields.Str()


class Typing(Schema):
    user_id: int = fields.Int()
    channel_id: int = fields.Int()
    member: 'GuildMember' = fields.Nested(GuildMember)
    timestamp: str = fields.Str()


class ForwardMessage(Schema):
    class Author(Schema):
        id: int = fields.Int()
        avatar: str = fields.Str()
        type: int = fields.Int()
        dname: str = fields.Str()

    class Attachment(Schema):
        id: int = fields.Int()
        filename: str = fields.Str()
        hash: str = fields.Str()
        type: str = fields.Str()
        size: int = fields.Int()
        width: int = fields.Int()
        height: int = fields.Int()
        url: str = fields.Str()

    id: int = fields.Int()
    content: str = fields.Str()
    stamps: List['Stamp'] = fields.Nested(Stamp)
    attachments: List['Attachment'] = fields.List(fields.Nested(Attachment))
    reply: 'Message' = fields.Nested(Message)
    timestamp: str = fields.Str()


class Forward(Schema):
    class Guild(Schema):
        id: int = fields.Int()
        name: str = fields.Str()

    class Channel(Schema):
        id: int = fields.Int()
        name: str = fields.Str()

    id: int = fields.Int()
    content: str = fields.Str()
    guild: Guild = fields.Nested(Guild)
    channel: Channel = fields.Nested(Channel)
    messages: List[ForwardMessage] = fields.List(fields.Nested(ForwardMessage))
    thumb: List['ForwardThumb'] = fields.List(fields.Nested(ForwardThumb))
