# -*- coding: utf-8 -*-

##################################################
# Event and EventDispatcher classes
##################################################

from typing import Any, Tuple, List, Dict

class Event(object):
    '''
    Generic evn to use with the EventDispatcher
    '''

    def __init__(self, event_type: str, data: Any =None):
        '''
        The constructor accepts and event type as string and a custom data
        '''
        self._type = event_type
        self._data = data
    
    @property
    def type(self):
        """
        Returns  the event type
        """
        return self._type
    
    @property
    def data(self):
        """
        Returns the data
        """
        return self._data


class EventDispatcher(object):
    '''
    Generic Event dispatcher which listens and dispatches events.
    '''
    def __init__(self):
        self._events = dict()
        
    def __del__(self):
        ''' 
        Remove all the listener references at destructions time
        '''
        self._events = None
        
    def has_listener(self, event_type, listener):
        '''
        Return true if listen is register to event_type
        '''
        if event_type in self._events.keys():
            return listener in self.events[event_type]
        else:
            return False
            
    def dispatch_event(self, event):
        ''' Dispatch an instance of Event Class
        '''
        # Dispatch the event to all associaciated listeners
        if event.type in self._events.keys():
            listeners = self._events[event.type]
            for listener in listeners:
                listener(event)
                
    def add_event_listener(self, event_type, listener):
        '''
        Add an event listener for an event type
        '''
        # Add listener to the event type
        if not self.has_listener(event_type, listener):
            listeners = self._events.get(event_type, []) # Get all the listeners for that event type or get an empty list
            listeners.append(listener)
            
            self._events[ event_type ] = listeners
            
    def remove_event_listener(self, event_type, listener):
        '''
        Remove event listener
        '''
        # Remove the listener from the event type
        if self.has_listener(event_type, listener):
            listeners = self._events[event_type ]
            
            if len(listeners) == 1:
                # Only this listener remains so remove the key
                del self._events[event_type]
                
            else:
                # Update listeners chain
                listener.remove(listener)
                
                self._events[ event_type]
                

class  Trigger(object):
    '''
    The trigger class
    '''
    def __init__(self, event_dispatcher, event):
        # Save a reference to the event dispatcher
        self.event_dispatcher = event_dispatcher 
        
        # Add the listener and event to the dispatcher
        #self.event_dispatcher.add_event_listener(event.type, event.data)
        self.event =  event
        
    def fire(self):
        '''
        Dispatch the fire event.
        '''
        self.event_dispatcher.dispatch_event(self.event)
        
    
class Listener(object):
    '''
    The listener class
    '''
    def __init__(self, event_dispatcher, event):
        # Save  event dipatcher reference
        self.event_dispatcher = event_dispatcher
        
        # Add the event
        self.event_dispatcher.add_event_listener(event.type, event.data)
        

