/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.vitv.presentationeditor;

import java.awt.Color;
import java.awt.Dimension;
import javax.swing.JPanel;

/**
 *
 * @author kpliuniverse
 */
public class CurCanvas {

    // The private static instance of the class (initialized to null).
    private static CurCanvas instance;

    
    //vars and stuff
    public Dimension size;
    public JPanel panel;
    // Private constructor to prevent instantiation from outside the class.
    private CurCanvas() {
        this.panel = new JPanel();
        this.panel.setBackground(Color.red);
        this.panel.setPreferredSize(new Dimension(300, 3000));
        this.panel.setLayout(null);
        
    }

    // Public method to access the instance.
    public static CurCanvas getInstance() {
        if (instance == null) {
            instance = new CurCanvas(); // Create the instance only when it's needed
        }
        return instance;
    }

    // Example method
    public void doSomething() {
        System.out.println("Canvas is doing something.");
    }
}
