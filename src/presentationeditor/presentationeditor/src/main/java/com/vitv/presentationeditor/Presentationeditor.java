/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 */

package com.vitv.presentationeditor;

import com.vitv.presentationeditor.DataClasses.InternalArgs.Args;
import com.vitv.presentationeditor.DataClasses.PresInfo.PresInfoMother;
import com.vitv.presentationeditor.XmlTools.ReadMother;

import lombok.AllArgsConstructor;

/**
 *
 * @author kpliuniverse
 */
public class Presentationeditor {

    

    public static void main(String[] cli_args) throws Exception {
        Args args = new Args();
        
        args.presInfoMother = ReadMother.readMotherXML();
        MainApp.main(args, cli_args);
    }
}
