/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Other/File.java to edit this template
 */
package com.vitv.presentationeditor;

/**
 *
 * @author kpliuniverse
 */
public class ErrEx {

    public static class SingletonNotManuallyInitializedError extends RuntimeException {

        public SingletonNotManuallyInitializedError() {
        }

        public SingletonNotManuallyInitializedError(String message) {
            super(message);
        }

        public SingletonNotManuallyInitializedError(String message, Throwable cause) {
            super(message, cause);
        }

        public SingletonNotManuallyInitializedError(Throwable cause) {
            super(cause);
        }

        public SingletonNotManuallyInitializedError(String message, Throwable cause, boolean enableSuppression, boolean writableStackTrace) {
            super(message, cause, enableSuppression, writableStackTrace);
        }
    };
}
