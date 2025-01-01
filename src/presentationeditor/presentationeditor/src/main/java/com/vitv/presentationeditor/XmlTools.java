package com.vitv.presentationeditor;


import javax.xml.stream.XMLInputFactory;
import javax.xml.stream.XMLStreamConstants;
import java.io.FileInputStream;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.xml.stream.XMLEventReader;
import javax.xml.stream.XMLStreamException;
import javax.xml.stream.events.XMLEvent;

public class XmlTools {
    
    public static void readMotherXMLIndiv(XMLEvent event) {
        
    }
    public static void readMotherXML() throws Exception {
        
        // Create an XML input factory
        XMLInputFactory factory = XMLInputFactory.newInstance();
        
        // Create an XMLStreamReader to read the XML
        XMLEventReader reader = factory.createXMLEventReader(new FileInputStream("s.xml"));

        String w = null;
        String h = null;
        
        StreamTools.CondIterator<XMLEvent> condIt = new StreamTools.CondIterator<>(reader::hasNext, () -> {
            try {
                return reader.nextEvent();
            } catch (XMLStreamException e) {
                throw new RuntimeException(e);  // Wrap the checked exception as an unchecked one
            }
        });
        
        
        StreamTools.forEach(XmlTools::readMotherXMLIndiv, reader, condIt);
        
    }
}
