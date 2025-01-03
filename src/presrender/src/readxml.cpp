#include "readxml.hpp"

#include "3rdparty/tinyxml2/tinyxml2.hpp"

#include <limits> 

#include "readxmlabbr.hpp"
#include "presdata.hpp"








#define macro_xml_check_result(a_eResult, errStr) if(a_eResult != tinyxml2::XML_SUCCESS) {printf("Error: %i\n", a_eResult); return readxml::xml_read_failure(a_eResult, errStr);}

bool readxml::isSuccessful(MotherResult motherResult) {
    return motherResult.result == tinyxml2::XML_SUCCESS;  // if no error, return true.
};

readxml::MotherResult readxml::xml_read_failure(tXMLError eResult, const char* errStr) {
    MotherResult result;
    result.result = eResult;
    result.errStr = errStr;
    return result;
}

readxml::MotherResult readxml::parse_xml() {
    //load from file
    const char* file = "labrats/in/testmother.xml";
    tXMLDocument xml_doc;
    macro_xml_check_result(xml_doc.LoadFile(file), xml_doc.ErrorStr());
    
    //parse
    tinyxml2::XMLElement* presRoot = xml_doc.FirstChildElement("pres");
    if (presRoot == nullptr) return xml_read_failure(tinyxml2::XML_ERROR_FILE_READ_ERROR, "Cannot find root");
    tXMLElement * infoElem = presRoot->FirstChildElement("info");
    if (infoElem == nullptr) return xml_read_failure(tinyxml2::XML_ERROR_PARSING_ELEMENT, "Error parsing element");

    presdata::PresDataMother out_value;

    macro_xml_check_result(infoElem->QueryUnsignedAttribute("h", &out_value.height), "Attr not found / Error parsing element \"h\"");
    macro_xml_check_result(infoElem->QueryUnsignedAttribute("w", &out_value.width), "Attr not found / Error parsing element \"w\""); 

    readxml::MotherResult out;
    out.result = tinyxml2::XML_SUCCESS;  // if no error, set result to success.
    out.value = out_value;
    return out;
}
