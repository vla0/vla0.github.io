# VLA-0: Building State-of-the-Art VLAs with Zero Modification

**Ankit Goyal, Hugo Hadfield, Xuning Yang, Valts Bulkis, Fabio Ramos**  
NVIDIA

---

## 🚀 Code Coming Soon!

We will release the code, trained models, and training scripts soon. Stay tuned!

## 📧 Contact

**For questions, please contact:**  
Ankit Goyal - [ankgoyal@umich.edu](mailto:ankgoyal@umich.edu)

---

## Abstract

Vision-Language-Action models (VLAs) hold immense promise for enabling generalist robot manipulation. However, the best way to build them remains an open question. Current approaches often add complexity, such as modifying the existing vocabulary of a Vision-Language Model (VLM) with action tokens or introducing special action heads. Curiously, the simplest strategy of representing actions directly as text has remained largely unexplored.

This work introduces **VLA-0** to investigate this idea. We find that VLA-0 is not only effective; it is surprisingly powerful. With the right design, VLA-0 outperforms more involved models. On LIBERO, a popular benchmark for evaluating VLAs, VLA-0 outperforms all existing methods trained on the same robotic data. Furthermore, without large-scale robotics-specific training, it outperforms methods trained on large-scale robotic data. These findings also translate to the real world, where VLA-0 outperforms SmolVLA, a VLA model pre-trained on large-scale real data.

---

## Key Results

- ✅ **Best performance** on LIBERO among models without large-scale pretraining (94.7% average success rate)
- ✅ **Outperforms** methods with large-scale pretraining (π₀, π₀.₅-KI, GR00T-N1, MolmoAct)
- ✅ **Superior real-world performance** (+12.5% over SmolVLA on SO-100 robot)
- ✅ **No architectural changes** to the base VLM required

---

## Resources

- **Paper:** [arXiv:2510.13054](https://arxiv.org/abs/2510.13054)
- **Website:** [https://vla0.github.io/](https://vla0.github.io/)
- **Code:** [https://github.com/NVlabs/vla0](https://github.com/NVlabs/vla0) (Coming soon!)

---

## Citation

If you find VLA-0 useful in your research, please consider citing:

```bibtex
@article{goyal2025vla0,
  title={VLA-0: Building State-of-the-Art VLAs with Zero Modification},
  author={Goyal, Ankit and Hadfield, Hugo and Yang, Xuning and Bulkis, Valts and Ramos, Fabio},
  journal={arXiv preprint arXiv:2510.13054},
  year={2025}
}
```