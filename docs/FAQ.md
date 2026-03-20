# FAQ

<details>
<summary><b>Why is there a separate Vector3 class instead of just using numpy or Python arrays?</b></summary>
<br>

To implement a dedicated Vector3 class was a conscious decision. It might make the code
slightly more verbose, but allows the code itself to directly differentiate for you where
you need to use a 3D vector, or a list with multiple entries. In other words, the code here
documents itself by using a named type system.
</details>

<br>

<details>
<summary><b>The text in my views or color bars is cropped away. How can i fix that?</b></summary>
<br>

When the problem is inside a TextView, you can either increase the size of the text view,
which gives the TextView more relative space to the other views. You can also make the font
size of the text smaller. Another possibility is to generally increase the height of the
layout. This increases the pixels of the image, while keeping the font sizes the same.

When the problem is inside a color bar, you can try the same things. Only difference is,
that you would set the font size inside the ColorMap you pass to the view the color bar belongs
to.
</details>

<br>
