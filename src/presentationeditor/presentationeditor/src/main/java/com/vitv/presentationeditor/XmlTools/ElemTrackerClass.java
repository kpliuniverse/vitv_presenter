/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Other/File.java to edit this template
 */
package com.vitv.presentationeditor.XmlTools;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.concurrent.Callable;
import java.util.function.BiConsumer;
import java.util.function.Consumer;
import javax.xml.stream.events.EndElement;
import javax.xml.stream.events.StartElement;
import javax.xml.stream.events.XMLEvent;
import lombok.AllArgsConstructor;

/**
 *
 * @author kpliuniverse
 */
public class ElemTrackerClass {
    
    
    
    @AllArgsConstructor
    public static class XMLElementRunner{
        String elemName;
        Consumer<StartElement> StartElementFn;
        Consumer<EndElement>  EndElementFn;
    }
    
    public static class ElemTracker {
        HashMap<String, XMLElementRunner> listElemToTrack = new HashMap<>();
        
        public ElemTracker() {
            
        }
        
        public void run(XMLEvent nextEvent) {
            if (nextEvent.isStartElement()) {
                StartElement startElement = nextEvent.asStartElement();
                String localPart = startElement.getName().getLocalPart();
                if(listElemToTrack.containsKey(localPart)) {
                    XMLElementRunner x = listElemToTrack.get(localPart);
                    x.StartElementFn.accept(startElement);
                }
            }
            if (nextEvent.isEndElement()) {
                EndElement endElement = nextEvent.asEndElement();
                String localPart = endElement.getName().getLocalPart();
                if(listElemToTrack.containsKey(localPart)) {
                    XMLElementRunner x = listElemToTrack.get(localPart);
                    x.EndElementFn.accept(endElement);
                }
            }
        }
        
        public void addElemToTrack(XMLElementRunner elemToTrack, boolean allowOverride)  {
            BiConsumer<String, XMLElementRunner> x = (allowOverride ? this.listElemToTrack::put :  this.listElemToTrack::putIfAbsent);
            x.accept(elemToTrack.elemName, elemToTrack);
   
        }
        
        public void addElemToTrack(XMLElementRunner elemToTrack) {
            this.addElemToTrack(elemToTrack, false);
        }
        
        public void clearElemToTrack() {
            listElemToTrack.clear();
        }
    }
}
