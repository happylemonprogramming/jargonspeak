#!/usr/bin/env python

import uuid

import tornado.ioloop
from rich.console import Console
from rich.table import Table
from tornado import gen

from pynostr.base_relay import RelayPolicy
from pynostr.event import EventKind
from pynostr.filters import Filters, FiltersList
from pynostr.message_pool import MessagePool
from pynostr.relay import Relay
from pynostr.utils import get_public_key

if __name__ == "__main__":

    console = Console()

    input_str = 'npub1hee433872q2gen90cqh2ypwcq9z7y5ugn23etrd2l2rrwpruss8qwmrsv6'
    recipient = ""
    author = get_public_key(input_str)

    # relay_url = input("relay: ")
    relay_url = 'wss://relay.damus.io'

    filters = FiltersList(
        [Filters(authors=[author.hex()], kinds=[EventKind.TEXT_NOTE], limit=100)]
    )

    subscription_id = uuid.uuid1().hex
    io_loop = tornado.ioloop.IOLoop.current()
    message_pool = MessagePool(first_response_only=False)
    policy = RelayPolicy()
    r = Relay(relay_url, message_pool, io_loop, policy, timeout=3)

    r.add_subscription(subscription_id, filters)

    try:
        io_loop.run_sync(r.connect)
    except gen.Return:
        pass
    io_loop.stop()

    event_msgs = message_pool.get_all_events()
    print(f"{r.url} returned {len(event_msgs)} TEXT_NOTEs from {input_str}.")

    # table = Table("date", "content")
    # for event_msg in event_msgs[::-1]:
    #     table.add_row(str(event_msg.event.date_time()), event_msg.event.content)
    # # console.print(table)

import streamlit as st
import re
from deepltranslate import texttranslate
from translatevideo import translatevideo

# Initialize a dictionary in session state to store content for each container
if 'content_dict' not in st.session_state:
    st.session_state.content_dict = {}

st.header('Nostr Client')
for i, event_msg in enumerate(event_msgs[::-1]):
    container_key = f'container_{i}'
    
    # Initialize content for the current container
    if container_key not in st.session_state.content_dict:
        st.session_state.content_dict[container_key] = event_msg.event.content
    
    with st.container():
        st.header(f'Note #{i+1}')
        
        # Translate button updates content for the current container
        if st.button('Translate', key=container_key):
            st.session_state.content_dict[container_key] = texttranslate(event_msg.event.content, 'es')
            # Display the updated content immediately
            st.text(st.session_state.content_dict[container_key])

            if 'mp4' in st.session_state.content_dict[container_key]:
                # Use regular expressions to find the video URL
                video_url = re.search(r'https://\S+', st.session_state.content_dict[container_key]).group(0)
                translatevideo(video_url, voice='Speaker', captions=False, filepath='files/client/', filename= f'note{i+1}.mp4', language='es')
                st.video(f'files/client/jargonspeak_note{i+1}.mp4')
            
            if 'jpg' in st.session_state.content_dict[container_key] or 'webp' in st.session_state.content_dict[container_key] or 'gif' in st.session_state.content_dict[container_key]:
                media_url = re.search(r'https://\S+', st.session_state.content_dict[container_key]).group(0)
                st.image(media_url)


        else:
            # Display the current content for the container
            st.text(st.session_state.content_dict[container_key])
        
            if 'mp4' in st.session_state.content_dict[container_key]:
                # Use regular expressions to find the video URL
                video_url = re.search(r'https://\S+', st.session_state.content_dict[container_key]).group(0)
                st.video(video_url)
            
            if 'jpg' in st.session_state.content_dict[container_key] or 'webp' in st.session_state.content_dict[container_key] or 'gif' in st.session_state.content_dict[container_key]:
                media_url = re.search(r'https://\S+', st.session_state.content_dict[container_key]).group(0)
                st.image(media_url)

