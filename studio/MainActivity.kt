package com.example.mindmap
import android.app.Activity
import android.os.Bundle
import android.content.Context
import android.view.View
import android.view.MotionEvent
import android.graphics.Canvas
import android.graphics.Path
import android.graphics.Paint
import android.graphics.Color

class MainActivity:Activity(){
    override fun onCreate(savedInstanceState:Bundle?){
        super.onCreate(savedInstanceState)
        val screen = CanvasScreen(this)
        setContentView(screen)
    }
}

class CanvasScreen(context:Context):View(context){
    private val paths = mutableListOf<Path>()
    private val pen = Paint().apply{
        color = Color.BLACK
        strokeWidth = 5f
        style = Paint.Style.STROKE
    }
    init{setBackgroundColor(Color.WHITE)}
    override fun onTouchEvent(event:MotionEvent):Boolean{
        when(event.actionMasked){
            MotionEvent.ACTION_DOWN->{paths.add(Path().apply{moveTo(event.x,event.y)})}
            MotionEvent.ACTION_MOVE->{paths.lastOrNull()?.lineTo(event.x,event.y)}  
            MotionEvent.ACTION_UP->{paths.lastOrNull()?.lineTo(event.x,event.y)}
        }
        invalidate()
        return true
    }
    override fun onDraw(canvas:Canvas){
        paths.forEach{canvas.drawPath(it,pen)}
    }
}