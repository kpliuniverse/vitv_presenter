package com.vitv.presentationeditor.XmlTools;


import com.vitv.presentationeditor.DataClasses.PresInfo.PresInfoMother;
import com.vitv.presentationeditor.MiscTools.StreamTools;
import com.vitv.presentationeditor.XmlTools.ElemTrackerClass.ElemTracker;
import com.vitv.presentationeditor.XmlTools.ElemTrackerClass.XMLElementRunner;

import javax.xml.stream.XMLInputFactory;
import javax.xml.stream.XMLStreamConstants;
import java.io.FileInputStream;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.xml.namespace.QName;
import javax.xml.stream.XMLEventReader;
import javax.xml.stream.XMLStreamException;
import javax.xml.stream.events.XMLEvent;
import lombok.AllArgsConstructor;

public class ReadMother {
    
    enum ReadMotherMainStatus {
        INFO,
        BODY
    }

    static class ReadMotherStatus {
        ReadMotherMainStatus mainStatus = ReadMotherMainStatus.INFO;
    }
    
    static ElemTracker setUpElemTracker(PresInfoMother result, ReadMotherContext context) {

        ElemTracker out = new ElemTracker();
        
        final XMLElementRunner readInfo = new XMLElementRunner(
            "info",
            (startElem) -> {
                
                
                switch (context.readMotherStatus.mainStatus) {
                    case INFO: {
                        result.width = Integer.parseInt(startElem.getAttributeByName(new QName("w")).getValue());
                        result.height = Integer.parseInt(startElem.getAttributeByName(new QName("h")).getValue());
                        context.readMotherStatus.mainStatus = ReadMotherMainStatus.BODY;
                    }
                    default: break;
                }

                

            },
            (_0) -> {
                
            }
        ); 
        out.addElemToTrack(readInfo);
        
        return out;
    }
    
    @AllArgsConstructor
    static class ReadMotherContext{
        ElemTracker elemTracker;
        
        ReadMotherStatus readMotherStatus;
    }
    
    static void readMotherXMLIndiv(XMLEvent event, PresInfoMother result, ReadMotherContext context) {
        context.elemTracker.run(event);
    }
    
    public static PresInfoMother readMotherXML() throws Exception {
        
        // Create an XML input factory;
        XMLInputFactory factory = XMLInputFactory.newInstance();
        
        // Create an XMLStreamReader to read the XML
        XMLEventReader reader = factory.createXMLEventReader(new FileInputStream("labrats/in/testmother.xml"));

        String w = "0";
        String h = "0";
        
        StreamTools.CondIterator<XMLEvent> condIt = new StreamTools.CondIterator<>(reader::hasNext, () -> {
            try {
                return reader.nextEvent();
            } catch (XMLStreamException e) {
                throw new RuntimeException("Error reading XML event", e);
            }
        });
        
        ReadMotherContext readMotherContext = new ReadMotherContext (
            null,
            new ReadMotherStatus()
        );
        
        
        PresInfoMother resultMut = new PresInfoMother(0, 0);
        readMotherContext.elemTracker = setUpElemTracker(resultMut, readMotherContext);
        StreamTools.forEach((XMLEvent x) -> ReadMother.readMotherXMLIndiv(x, resultMut, readMotherContext), reader, condIt);
        return resultMut;
        
        
        
        

        
    }
}
