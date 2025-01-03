#include "3rdparty/tinyxml2/tinyxml2.hpp"
#include "readxmlabbr.hpp"
#include "presdata.hpp"


#ifndef VITV_READXML
#define VITV_READXML



namespace readxml {




struct VitVReadMotherInfo {
    
};


struct MotherResult {
    tXMLError result;
    presdata::PresDataMother value;
    const char* errStr;
};

bool isSuccessful(MotherResult motherResult);

MotherResult xml_read_failure(tXMLError eResult, const char* errStr);

MotherResult parse_xml();

}
#endif